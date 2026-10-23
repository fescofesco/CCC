"""Line-sweep strategy for level 6.

The two emitters of one family (e.g. 1 and 4 for rows) placed on the same line
give every cell of that line two beams, so the whole line fills in one tick.
"Cutter" emitters from the other families cross the line at its halo cells and
raise them to three beams, which keeps them empty. The sweep visits every line
of the pattern that has no more halo cells than there are cutters, moving the
emitters between consecutive fill states with the cheapest instruction template
whose intermediate states are all safe. Cells on lines that cannot be filled
this way are left for the greedy painter.
"""
from __future__ import annotations

from collections import Counter
from itertools import permutations, product

from hexboard import CORNER_INDEX, DIRECTIONS, border_ring, parse, ray, render

FAMILY = {1: 0, 4: 0, 2: 1, 5: 1, 3: 2, 6: 2}
SWEEP_CONFIGS = [
    (fill, cutters)
    for fill in ((1, 4), (2, 5), (3, 6))
    for cutters in ([c for c in ((1, 4), (2, 5), (3, 6)) if c != fill][0],
                    [c for c in ((1, 4), (2, 5), (3, 6)) if c != fill][1],
                    tuple(k for c in ((1, 4), (2, 5), (3, 6)) if c != fill for k in c))
]


class Beams:
    """Geometry and state safety for an arbitrary set of emitters (ring positions)."""

    def __init__(self, r: int, emitters):
        self.r = r
        self.n = 6 * r
        self.W = 2 * r - 1
        self.E = tuple(emitters)
        ring = border_ring(r)
        empty = parse(render(r).split("\n"))
        self.rays, self.line_id, self.cover, self.lo, self.allowed = {}, {}, {}, {}, {}
        for k in self.E:
            rays = [frozenset(ray(empty, *ring[i], DIRECTIONS[k], passable="O")) for i in range(self.n)]
            useful = [i for i in range(self.n) if rays[i]]
            lo = next(i for i in useful if not rays[(i - 1) % self.n])
            self.lo[k] = lo
            self.rays[k] = rays
            self.line_id[k] = [min(s) if s else None for s in rays]
            self.cover[k] = {c: i for i in useful for c in rays[i]}
            self.allowed[k] = {(lo + u) % self.n for u in range(-1, self.W + 1)}
        pairs = [(x, y) for i, x in enumerate(self.E) for y in self.E[i + 1 :]]
        self.same = [(x, y) for x, y in pairs if FAMILY[x] == FAMILY[y]]
        self.crossp = [(x, y) for x, y in pairs if FAMILY[x] != FAMILY[y]]
        self.cross = {}
        for x, y in self.crossp:
            table = {}
            for px in self.allowed[x]:
                rx = self.rays[x][px]
                if rx:
                    for py in self.allowed[y]:
                        common = rx & self.rays[y][py]
                        if common:
                            table[(px, py)] = next(iter(common))
            self.cross[(x, y)] = table

    def offset(self, k: int, pos: int) -> int:
        return ((pos - self.lo[k] + 1) % self.n) - 1

    def position(self, k: int, offset: int) -> int:
        return (self.lo[k] + offset) % self.n

    def painted(self, pos: dict, on: dict, P: set, halo: set):
        """Cells with exactly two beams, or None if the state is unsafe."""
        beams = [k for k in self.E if on[k]]
        coincide = any(
            on[x] and on[y] and self.line_id[x][pos[x]] is not None and self.line_id[x][pos[x]] == self.line_id[y][pos[y]]
            for x, y in self.same
        )
        if coincide:
            hits: Counter = Counter()
            for k in beams:
                hits.update(self.rays[k][pos[k]])
            items = hits.items()
        else:
            cand = set()
            for x, y in self.crossp:
                if on[x] and on[y]:
                    c = self.cross[(x, y)].get((pos[x], pos[y]))
                    if c is not None:
                        cand.add(c)
            items = [(c, sum(1 for k in beams if c in self.rays[k][pos[k]])) for c in cand]
        painted = []
        for c, cnt in items:
            if cnt == 2:
                if c in halo:
                    return None
                painted.append(c)
            elif cnt >= 3 and c in P:
                return None
        return painted


def instruction_lines(beams: Beams, schedule: dict, D: int) -> list[list[str]]:
    """schedule[k] = list of (tick, instruction) for emitter k; other ticks are no-ops."""
    lines = [["-"] * 6 for _ in range(D)]
    for k, events in schedule.items():
        for t, ins in events:
            lines[t][k - 1] = ins
    return lines


def apply_line(beams: Beams, pos: dict, on: dict, line: list[str]):
    pos, on = dict(pos), dict(on)
    for k in beams.E:
        ins = line[k - 1]
        if ins == "T":
            on[k] = not on[k]
        elif ins in "FB":
            p = (pos[k] + (1 if ins == "F" else -1)) % beams.n
            if p not in beams.allowed[k]:
                return None
            pos[k] = p
    return pos, on


def safe_sequence(beams: Beams, pos: dict, on: dict, lines: list[list[str]], P: set, halo: set):
    """Apply lines; return the end state if every intermediate state is safe, else None."""
    for line in lines:
        state = apply_line(beams, pos, on, line)
        if state is None:
            return None
        pos, on = state
        if beams.painted(pos, on, P, halo) is None:
            return None
    return pos, on


def transition(beams: Beams, pos: dict, on: dict, target: dict, fill, P: set, halo: set):
    """Shortest safe instruction template from (pos, on) to the fill state at `target` (all on)."""
    E = beams.E
    delta = {k: beams.offset(k, target[k]) - beams.offset(k, pos[k]) for k in E}
    dist = {k: abs(delta[k]) for k in E}
    step = {k: "F" if delta[k] > 0 else "B" for k in E}
    others = [k for k in E if k not in fill]

    def moves(k, start):
        return [(start + i, step[k]) for i in range(dist[k])]

    # all emitters stay on: try every early/late scheduling of the moves
    D = max(dist.values())
    if D > 0 and all(on.values()):
        for timing in product((0, 1), repeat=len(E)):
            schedule = {k: moves(k, 0 if early == 0 else D - dist[k]) for k, early in zip(E, timing)}
            lines = instruction_lines(beams, schedule, D)
            end = safe_sequence(beams, pos, on, lines, P, halo)
            if end is not None:
                return lines, end
    # switch the fill emitters off while everything moves, on again at the fill tick
    df = max(dist[k] for k in fill)
    dc = max((dist[k] for k in others), default=0)
    D = max(dc, df + 2, 2)
    for timing in product((0, 1), repeat=len(others)):
        schedule = {}
        for k in fill:
            events = []
            if on[k]:
                events.append((0, "T"))
                events += moves(k, 1)
            else:
                events += moves(k, 0)
            events.append((D - 1, "T"))
            schedule[k] = events
        for k, early in zip(others, timing):
            events = moves(k, 0 if early == 0 else D - dist[k])
            if not on[k]:
                events.append((D - 1, "T"))  # switch cutters on at the fill tick
            schedule[k] = events
        lines = instruction_lines(beams, schedule, D)
        end = safe_sequence(beams, pos, on, lines, P, halo)
        if end is not None:
            return lines, end
    return None


def sweep_pass(r: int, cells: set, halo: set, fill=(1, 4), cutters=(3, 6), direction: int = 1, max_lines: int = 0):
    """Returns (lines, end_pos, end_on, leftover cells) or None if nothing could be filled.
    With max_lines > 0 the sweep stops after that many filled lines (used to seed other searches)."""
    beams = Beams(r, tuple(fill) + tuple(cutters))
    f1, f2 = fill
    P = set(cells)
    line_pos_f2 = {beams.line_id[f2][p]: p for p in beams.allowed[f2] if beams.line_id[f2][p] is not None}
    lines_of_fill = []
    for u in range(beams.W):
        p1 = beams.position(f1, u)
        line_cells = beams.rays[f1][p1]
        if line_cells & P:
            lines_of_fill.append((p1, line_pos_f2[beams.line_id[f1][p1]], line_cells))
    if direction < 0:
        lines_of_fill.reverse()

    pos = {k: CORNER_INDEX[k] * r for k in beams.E}
    on = {k: False for k in beams.E}
    program: list[list[str]] = []
    painted_total: set = set()
    filled = 0

    for p1, p2, line_cells in lines_of_fill:
        H = sorted(c for c in line_cells if c in halo)
        if len(H) > len(cutters):
            continue
        best = None
        for assignment in permutations(cutters, len(H)):
            target = {f1: p1, f2: p2}
            for c, h in zip(assignment, H):
                target[c] = beams.cover[c][h]
            ok = True
            for c in cutters:
                if c in assignment:
                    continue
                # park a spare cutter on the nearest line that meets this fill line only in far cells
                options = []
                for q in beams.allowed[c]:
                    meet = beams.rays[c][q] & line_cells
                    if not meet or not (meet & P or meet & halo):
                        options.append((abs(beams.offset(c, q) - beams.offset(c, pos[c])), q))
                if not options:
                    ok = False
                    break
                target[c] = min(options)[1]
            if not ok:
                continue
            all_on = {k: True for k in beams.E}
            if beams.painted(target, all_on, P, halo) is None:
                continue
            cost = max(abs(beams.offset(k, target[k]) - beams.offset(k, pos[k])) for k in beams.E)
            if best is None or cost < best[0]:
                best = (cost, target)
        if best is None:
            continue
        result = transition(beams, pos, on, best[1], fill, P, halo)
        if result is None:
            continue
        lines, (pos, on) = result
        program += lines
        painted_total |= line_cells - set(H)
        filled += 1
        if max_lines and filled >= max_lines:
            break

    if not program:
        return None
    return program, pos, on, P - painted_total
