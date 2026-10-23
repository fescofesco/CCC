"""Greedy multi-beam painter for level 6.

Four main emitters from two direction families (e.g. rows 1/4 and SW diagonals
3/6) are moved one ring step per tick. Their beams meet in up to four cells (the
corners of a "rectangle" in line space), and when the two emitters of one family
sit on the same line that whole line fills, cut where the other family's beams
cross it. Optionally the two emitters of the third family join in as "extra"
beams: they are only switched on in ticks where all of their crossings are safe
and paint new cells, and are nudged off again once they stop contributing.

Each tick the painter tries every combination of moves and toggles for the main
emitters (and, for the most promising ones, of the extra emitters) and keeps the
safe combination that paints the most missing pattern cells, breaking ties by a
distance heuristic, a random seed and optionally a one-tick lookahead.

Safety is a property of the emitter state alone (never paint a halo cell, never
hit a pattern cell with three or more beams), so the generated instruction
sequence can be played backwards for the next pass as well.
"""
from __future__ import annotations

import random
from collections import Counter
from itertools import product

from hexboard import CORNER_INDEX, DIRECTIONS, border_ring, parse, ray, render

ACTIONS = (-1, 0, 1, "T")
COMBOS4 = list(product(ACTIONS, repeat=4))
COMBOS2 = [c for c in product(ACTIONS, repeat=2) if c != (0, 0)]
FAMILY = {1: 0, 4: 0, 2: 1, 5: 1, 3: 2, 6: 2}
EMITTER_SETS = [(1, 4, 3, 6), (1, 4, 2, 5), (2, 5, 3, 6)]  # (family A pair, family B pair)


def third_family(emitters) -> tuple[int, int]:
    used = {FAMILY[k] for k in emitters}
    fam = ({0, 1, 2} - used).pop()
    return tuple(k for k in (1, 2, 3, 4, 5, 6) if FAMILY[k] == fam)


class Painter:
    def __init__(self, r: int, cells, halo: set, emitters=(1, 4, 3, 6), extra=()):
        self.r = r
        self.n = 6 * r
        self.W = 2 * r - 1
        self.main = tuple(emitters)
        self.extra = tuple(extra)
        self.E = self.main + self.extra
        assert len(self.main) == 4
        self.family_a = (self.main[0], self.main[1])
        self.family_b = (self.main[2], self.main[3])
        self.cursors = [(self.main[0], self.main[2]), (self.main[1], self.main[3])]
        pairs = [(x, y) for i, x in enumerate(self.E) for y in self.E[i + 1 :]]
        self.same_family = [(x, y) for x, y in pairs if FAMILY[x] == FAMILY[y]]
        self.cross_pairs = [(x, y) for x, y in pairs if FAMILY[x] != FAMILY[y]]
        ring = border_ring(r)
        empty = parse(render(r).split("\n"))
        self.rays: dict[int, list[frozenset]] = {}
        self.line_id: dict[int, list] = {}
        self.cover: dict[int, dict] = {}
        self.lo: dict[int, int] = {}
        self.allowed: dict[int, set] = {}
        for k in self.E:
            rays = [frozenset(ray(empty, *ring[i], DIRECTIONS[k], passable="O")) for i in range(self.n)]
            useful = [i for i in range(self.n) if rays[i]]
            lo = next(i for i in useful if not rays[(i - 1) % self.n])
            self.lo[k] = lo
            self.rays[k] = rays
            self.line_id[k] = [min(s) if s else None for s in rays]
            self.cover[k] = {c: i for i in useful for c in rays[i]}
            self.allowed[k] = {(lo + u) % self.n for u in range(-1, self.W + 1)}
        self.cross: dict[tuple[int, int], dict] = {}
        for x, y in self.cross_pairs:
            table = {}
            for px in self.allowed[x]:
                rx = self.rays[x][px]
                if not rx:
                    continue
                for py in self.allowed[y]:
                    common = rx & self.rays[y][py]
                    if common:
                        table[(px, py)] = next(iter(common))
            self.cross[(x, y)] = table
        self.P = set(cells)
        self.halo = halo
        self.pos = {k: CORNER_INDEX[k] * r for k in self.E}
        self.on = {k: False for k in self.E}

    def offset(self, k: int) -> int:
        """Ring position of emitter k as an offset along its useful arc (-1 .. W)."""
        return ((self.pos[k] - self.lo[k] + 1) % self.n) - 1

    def ring_dist(self, a: int, b: int) -> int:
        d = abs(a - b) % self.n
        return min(d, self.n - d)

    def painted_cells(self, pos: dict, on: dict):
        """Cells hit by exactly two beams, or None if the state is unsafe."""
        rays = self.rays
        beams = [k for k in self.E if on[k]]
        coincide = False
        for x, y in self.same_family:
            if on[x] and on[y] and self.line_id[x][pos[x]] is not None and self.line_id[x][pos[x]] == self.line_id[y][pos[y]]:
                coincide = True
        if coincide:
            hits: Counter = Counter()
            for k in beams:
                hits.update(rays[k][pos[k]])
            items = hits.items()
        else:
            cand = set()
            for x, y in self.cross_pairs:
                if on[x] and on[y]:
                    c = self.cross[(x, y)].get((pos[x], pos[y]))
                    if c is not None:
                        cand.add(c)
            items = [(c, sum(1 for k in beams if c in rays[k][pos[k]])) for c in cand]
        painted = []
        for c, cnt in items:
            if cnt == 2:
                if c in self.halo:
                    return None
                painted.append(c)
            elif cnt >= 3 and c in self.P:
                return None
        return painted

    def apply(self, pos: dict, on: dict, emitters, combo):
        """State after the given actions of `emitters`, or None if a move leaves an arc."""
        newpos, newon = dict(pos), dict(on)
        for k, act in zip(emitters, combo):
            if act == "T":
                newon[k] = not on[k]
            elif act:
                p = (pos[k] + act) % self.n
                if p not in self.allowed[k]:
                    return None
                newpos[k] = p
        return newpos, newon

    def candidates(self, pos: dict, on: dict, missing: set, top_extra: int = 12):
        """Safe (actions, newpos, newon, painted, gain, toggles) tuples for one tick."""
        out = []
        for combo in COMBOS4:
            state = self.apply(pos, on, self.main, combo)
            if state is None:
                continue
            painted = self.painted_cells(*state)
            if painted is None:
                continue
            gain = sum(1 for c in painted if c in missing)
            actions = dict(zip(self.main, combo))
            out.append((actions, state[0], state[1], painted, gain, combo.count("T")))
        if self.extra and out:
            out.sort(key=lambda s: -s[4])
            extended = []
            for actions, npos, non, painted, gain, toggles in out[:top_extra]:
                for combo in COMBOS2:
                    state = self.apply(npos, non, self.extra, combo)
                    if state is None:
                        continue
                    painted2 = self.painted_cells(*state)
                    if painted2 is None:
                        continue
                    gain2 = sum(1 for c in painted2 if c in missing)
                    acts = dict(actions)
                    acts.update(zip(self.extra, combo))
                    extended.append((acts, state[0], state[1], painted2, gain2, toggles + combo.count("T")))
            out += extended
        return out

    def run(self, max_stuck: int, heuristic: str = "cursor", seed: int = 0, lookahead: int = 0, top: int = 6,
            missing: set | None = None):
        """Paint greedily (from the current emitter state) until every missing cell has been painted
        or no progress was made for max_stuck ticks (then roll back to the last productive tick).
        Returns (instruction lines, cells still missing)."""
        rng = random.Random(seed)
        n = self.n
        missing = set(self.P) if missing is None else set(missing)
        lines: list[list[str]] = []
        checkpoint = (dict(self.pos), dict(self.on), set(missing), 0)
        stuck = 0
        while missing:
            if heuristic == "cursor":
                near = []
                for a, b in self.cursors:
                    table = {}
                    for da in (-1, 0, 1):
                        pa = (self.pos[a] + da) % n
                        for db in (-1, 0, 1):
                            pb = (self.pos[b] + db) % n
                            table[(da, db)] = min(
                                max(self.ring_dist(pa, self.cover[a][c]), self.ring_dist(pb, self.cover[b][c])) for c in missing
                            )
                    near.append(table)

                def h_of(actions, newpos, newon, painted):
                    h = 0
                    for (a, b), table in zip(self.cursors, near):
                        da = actions.get(a, 0)
                        db = actions.get(b, 0)
                        h += table[(0 if da == "T" else da, 0 if db == "T" else db)]
                    h += 2 * sum(1 for k in self.main if not newon[k])
                    return h + self.extra_penalty(newpos, newon, painted)
            else:
                near_e = {}
                for k in self.main:
                    for d in (-1, 0, 1):
                        p = (self.pos[k] + d) % n
                        near_e[(k, d)] = min(self.ring_dist(p, self.cover[k][c]) for c in missing)

                def h_of(actions, newpos, newon, painted):
                    h = 0
                    for k in self.main:
                        act = actions.get(k, 0)
                        h += near_e[(k, 0 if act == "T" else act)]
                    h += 2 * sum(1 for k in self.main if not newon[k])
                    return h + self.extra_penalty(newpos, newon, painted)

            scored = []
            for actions, newpos, newon, painted, gain, toggles in self.candidates(self.pos, self.on, missing):
                scored.append(((-gain, h_of(actions, newpos, newon, painted), toggles, rng.random()), actions, newpos, newon, painted, gain))
            scored.sort(key=lambda s: s[0])
            if lookahead and len(scored) > 1:
                best = None
                for entry in scored[:top]:
                    key, actions, newpos, newon, painted, gain = entry
                    left = missing.difference(painted)
                    future = max((g for *_, g, _t in self.candidates(newpos, newon, left)), default=0) if left else 0
                    key2 = (-(gain + future), key[1], key[2], key[3])
                    if best is None or key2 < best[0]:
                        best = (key2, entry)
                _, (key, actions, newpos, newon, painted, gain) = best
            else:
                key, actions, newpos, newon, painted, gain = scored[0]

            line = ["-"] * 6
            for k, act in actions.items():
                line[k - 1] = "T" if act == "T" else "F" if act == 1 else "B" if act == -1 else "-"
            lines.append(line)
            self.pos, self.on = newpos, newon
            missing.difference_update(painted)
            if gain:
                stuck = 0
                checkpoint = (dict(self.pos), dict(self.on), set(missing), len(lines))
            else:
                stuck += 1
                if stuck > max_stuck:
                    self.pos, self.on, missing, cut = checkpoint
                    lines = lines[:cut]
                    break
        return lines, missing

    def make_h(self, pos: dict, missing: set, heuristic: str):
        """Distance heuristic for the moves out of `pos` (lower is better)."""
        n = self.n
        if heuristic == "cursor":
            near = []
            for a, b in self.cursors:
                table = {}
                for da in (-1, 0, 1):
                    pa = (pos[a] + da) % n
                    for db in (-1, 0, 1):
                        pb = (pos[b] + db) % n
                        table[(da, db)] = min(
                            max(self.ring_dist(pa, self.cover[a][c]), self.ring_dist(pb, self.cover[b][c])) for c in missing
                        )
                near.append(table)

            def h_of(actions, newpos, newon, painted):
                h = 0
                for (a, b), table in zip(self.cursors, near):
                    da = actions.get(a, 0)
                    db = actions.get(b, 0)
                    h += table[(0 if da == "T" else da, 0 if db == "T" else db)]
                h += 2 * sum(1 for k in self.main if not newon[k])
                return h + self.extra_penalty(newpos, newon, painted)
        else:
            near_e = {}
            for k in self.main:
                for d in (-1, 0, 1):
                    p = (pos[k] + d) % n
                    near_e[(k, d)] = min(self.ring_dist(p, self.cover[k][c]) for c in missing)

            def h_of(actions, newpos, newon, painted):
                h = 0
                for k in self.main:
                    act = actions.get(k, 0)
                    h += near_e[(k, 0 if act == "T" else act)]
                h += 2 * sum(1 for k in self.main if not newon[k])
                return h + self.extra_penalty(newpos, newon, painted)
        return h_of

    def beam(self, width: int, max_ticks: int, heuristic: str = "cursor", seed: int = 0, missing: set | None = None):
        """Beam search over ticks: keep the `width` best states (fewest missing cells, then the
        distance heuristic). Returns (instruction lines, cells still missing); the search fails
        (missing non-empty) when no state finishes within max_ticks."""
        rng = random.Random(seed)
        missing0 = frozenset(self.P if missing is None else missing)
        states = [(dict(self.pos), dict(self.on), missing0, [])]
        best_partial = states[0]
        for _tick in range(max_ticks):
            expanded = []
            seen = set()
            for pos, on, miss, lines in states:
                h_of = self.make_h(pos, miss, heuristic)
                for actions, newpos, newon, painted, _gain, toggles in self.candidates(pos, on, miss):
                    newmiss = miss.difference(painted)
                    sig = (tuple(newpos[k] for k in self.E), tuple(newon[k] for k in self.E), newmiss)
                    if sig in seen:
                        continue
                    seen.add(sig)
                    line = ["-"] * 6
                    for k, act in actions.items():
                        line[k - 1] = "T" if act == "T" else "F" if act == 1 else "B" if act == -1 else "-"
                    key = (len(newmiss), h_of(actions, newpos, newon, painted), toggles, rng.random())
                    expanded.append((key, newpos, newon, newmiss, lines + [line]))
            if not expanded:
                break
            expanded.sort(key=lambda e: e[0])
            states = [(p, o, m, l) for _k, p, o, m, l in expanded[:width]]
            for pos, on, miss, lines in states:
                if not miss:
                    self.pos, self.on = pos, on
                    return lines, set()
            if len(states[0][2]) < len(best_partial[2]):
                best_partial = states[0]
        pos, on, miss, lines = best_partial
        self.pos, self.on = pos, on
        return lines, set(miss)

    def extra_penalty(self, newpos: dict, newon: dict, painted: list) -> int:
        """Extra emitters that are on but whose beams paint nothing are a liability."""
        penalty = 0
        for k in self.extra:
            if newon[k]:
                ray_cells = self.rays[k][newpos[k]]
                if not any(c in ray_cells for c in painted):
                    penalty += 1
        return penalty
