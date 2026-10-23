"""Level 6 - write a short program that submits each pattern K times (optimization level).

Two strategies produce one "pass" (a program that paints the whole pattern
once); the shorter verified result wins per board:

* single cursor (this file): with exactly two active beams, matter appears only
  at their crossing cell, so a pair of emitters from different direction
  families acts as a cursor that writes one cell per tick. Each emitter moves
  one border cell per tick, so the cursor makes king moves in the (line of p,
  line of q) configuration grid. It must never land on a halo cell (an empty
  cell touching the pattern), because that would block the pick-up arm; landing
  on far cells or outside the board is harmless. Where the halo is in the way,
  one emitter is switched off for the move (2 extra ticks). The cells are
  ordered into a short path (nearest neighbour + 2-opt + or-opt).
* greedy painter (painter.py): four beams paint up to four cells per tick, or a
  whole line when two emitters of one family share it. Cells the painter cannot
  reach are finished by the single cursor.

A pass is expanded to K passes by replaying it backwards and forwards (safety
only depends on the emitter state, so a reversed pass is valid too), with an
idle tick at each pass boundary to re-create the cell the arm just removed. The
program is cut right after the K-th submission and verified with the level 5
engine before it is written.
"""
from __future__ import annotations

import random
import sys
import time
from collections import deque

from ccc import blocks, run_level
from fabricator import Fabricator
from hexboard import CORNER_INDEX, DIRECTIONS, Grid, border_ring, find_all, in_bounds, parse, ray, render
from level5 import count_submissions
from painter import EMITTER_SETS, Painter, third_family
from shorten import ALL_EMITTERS, shorten
from sweep import SWEEP_CONFIGS, Beams, sweep_pass

INF = 10**9
PAIRS = [(p, q) for p in (1, 4) for q in (2, 3, 5, 6)] + [(p, q) for p in (2, 5) for q in (3, 6)]
REVERSE = {"F": "B", "B": "F", "T": "T", "-": "-"}
IDLE = ["-"] * 6
random.seed(42)


# ---------------------------------------------------------------------------------------------
# single cursor
# ---------------------------------------------------------------------------------------------
class Cursor:
    """Geometry of one emitter pair (p, q) on a radius-r board.

    Each emitter has a contiguous arc of 2r-1 useful ring positions whose beam enters the board.
    Positions are handled as offsets u along that arc (with a margin of one harmless position on
    either side). cross[(u_p, u_q)] is the cell where the two beams meet, or None."""

    def __init__(self, r: int, p: int, q: int):
        self.r, self.p, self.q = r, p, q
        self.n = 6 * r
        self.W = 2 * r - 1
        self.ring = border_ring(r)
        empty = parse(render(r).split("\n"))
        self.lo: dict[int, int] = {}
        self.start: dict[int, int] = {}
        self.rays: dict[int, dict[int, frozenset]] = {}
        for k in (p, q):
            rays = [frozenset(ray(empty, *self.ring[i], DIRECTIONS[k], passable="O")) for i in range(self.n)]
            useful = [i for i in range(self.n) if rays[i]]
            arc_starts = [i for i in useful if not rays[(i - 1) % self.n]]
            assert len(arc_starts) == 1 and len(useful) == self.W, (r, k)
            lo = arc_starts[0]
            self.lo[k] = lo
            self.rays[k] = {u: rays[(lo + u) % self.n] for u in range(-1, self.W + 1)}
            start = (CORNER_INDEX[k] * r - lo) % self.n
            assert 0 <= start < self.W, (r, k)
            self.start[k] = start
        self.cover = {k: {c: u for u in range(self.W) for c in self.rays[k][u]} for k in (p, q)}
        self.cross: dict[tuple[int, int], tuple[int, int] | None] = {}
        for up in range(-1, self.W + 1):
            for uq in range(-1, self.W + 1):
                common = self.rays[p][up] & self.rays[q][uq]
                assert len(common) <= 1
                self.cross[(up, uq)] = next(iter(common)) if common else None

    def config(self, cell: tuple[int, int]) -> tuple[int, int]:
        return (self.cover[self.p][cell], self.cover[self.q][cell])


def jump_cost(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Move with one emitter switched off (T, moves, T): no crossings happen on the way."""
    dp, dq = abs(a[0] - b[0]), abs(a[1] - b[1])
    return min(max(dp, dq + 2), max(dp + 2, dq))


class Planner:
    """Orders the cells for one cursor and writes the instruction lines of a single pass."""

    def __init__(self, cursor: Cursor, cells: list[tuple[int, int]], halo: set, k: int,
                 start_cfg: tuple[int, int] | None = None, on: tuple[bool, bool] = (False, False)):
        self.cur = cursor
        self.k = k
        self.cells = cells
        self.cfgs = [cursor.config(c) for c in cells]
        self.forbidden = {cfg for cfg, cell in cursor.cross.items() if cell in halo}
        self.start_cfg = start_cfg if start_cfg is not None else (cursor.start[cursor.p], cursor.start[cursor.q])
        self.on = on
        m = len(cells)
        self.D = [[0] * m for _ in range(m)]
        for i, cfg in enumerate(self.cfgs):
            dist, _ = self.bfs(cfg)
            row = self.D[i]
            for j, other in enumerate(self.cfgs):
                row[j] = min(dist.get(other, INF), jump_cost(cfg, other))
        s = self.start_cfg
        if all(on):  # both beams on: moving is a normal transition
            dist, _ = self.bfs(s)
            self.setup = [min(dist.get(c, INF), jump_cost(s, c)) for c in self.cfgs]
        else:  # at most one beam on: moves are free, one tick to switch on at the end
            self.setup = [max(abs(c[0] - s[0]), abs(c[1] - s[1])) + 1 for c in self.cfgs]

    def bfs(self, src):
        """King-move BFS over configurations that avoid the halo."""
        W = self.cur.W
        forbidden = self.forbidden
        dist = {src: 0}
        parent = {src: None}
        queue = deque([src])
        while queue:
            node = queue.popleft()
            d = dist[node] + 1
            up, uq = node
            for dp in (-1, 0, 1):
                np_ = up + dp
                if np_ < -1 or np_ > W:
                    continue
                for dq in (-1, 0, 1):
                    nq = uq + dq
                    if (dp == 0 and dq == 0) or nq < -1 or nq > W:
                        continue
                    nxt = (np_, nq)
                    if nxt in dist or nxt in forbidden:
                        continue
                    dist[nxt] = d
                    parent[nxt] = node
                    queue.append(nxt)
        return dist, parent

    # ---- tour construction -------------------------------------------------------------
    def cost(self, path: list[int]) -> int:
        length = sum(self.D[a][b] for a, b in zip(path, path[1:]))
        return self.setup[path[0]] + self.k * length + (self.k - 1)

    def nearest_neighbour(self, start: int) -> list[int]:
        m = len(self.cells)
        D = self.D
        left = set(range(m))
        left.remove(start)
        path = [start]
        while left:
            last = path[-1]
            nxt = min(left, key=lambda j: D[last][j])
            left.remove(nxt)
            path.append(nxt)
        return path

    def improve(self, path: list[int]) -> list[int]:
        D, k, setup = self.D, self.k, self.setup
        m = len(path)
        improved = True
        while improved:
            improved = False
            # 2-opt on an open path (i = -1 means the reversed segment starts at the first node)
            for i in range(-1, m - 2):
                a = path[i] if i >= 0 else None
                b = path[i + 1]
                for j in range(i + 2, m):
                    c = path[j]
                    d = path[j + 1] if j + 1 < m else None
                    old = (D[a][b] if a is not None else 0) + (D[c][d] if d is not None else 0)
                    new = (D[a][c] if a is not None else 0) + (D[b][d] if d is not None else 0)
                    delta = k * (new - old)
                    if a is None:
                        delta += setup[c] - setup[b]
                    if delta < 0:
                        path[i + 1 : j + 1] = path[i + 1 : j + 1][::-1]
                        improved = True
                        b = path[i + 1]
            # or-opt: relocate a single node
            for x in range(m):
                node = path[x]
                prev = path[x - 1] if x > 0 else None
                nxt = path[x + 1] if x + 1 < m else None
                removed = k * ((D[prev][node] if prev is not None else 0) + (D[node][nxt] if nxt is not None else 0)
                               - (D[prev][nxt] if prev is not None and nxt is not None else 0))
                if prev is None and nxt is not None:
                    removed += setup[node] - setup[nxt]
                rest = path[:x] + path[x + 1 :]
                best_gain, best_pos = 0, None
                for y in range(len(rest) + 1):
                    u = rest[y - 1] if y > 0 else None
                    v = rest[y] if y < len(rest) else None
                    added = k * ((D[u][node] if u is not None else 0) + (D[node][v] if v is not None else 0)
                                 - (D[u][v] if u is not None and v is not None else 0))
                    if u is None and v is not None:
                        added += setup[node] - setup[v]
                    gain = removed - added
                    if gain > best_gain:
                        best_gain, best_pos = gain, y
                if best_pos is not None:
                    path = rest[:best_pos] + [node] + rest[best_pos:]
                    improved = True
        return path

    def best_path(self, starts: int) -> list[int]:
        m = len(self.cells)
        candidates = list(range(m)) if m <= starts else random.sample(range(m), starts)
        best, best_cost = None, INF
        for s in candidates:
            path = self.improve(self.nearest_neighbour(s))
            c = self.cost(path)
            if c < best_cost:
                best, best_cost = path, c
        return best

    # ---- program generation (one pass) --------------------------------------------------
    def program(self, path: list[int]) -> list[list[str]]:
        cur = self.cur
        p, q = cur.p, cur.q
        lines: list[list[str]] = []

        def line(instr: dict[int, str]) -> list[str]:
            out = ["-"] * 6
            for emitter, ins in instr.items():
                out[emitter - 1] = ins
            return out

        def step(delta: int) -> str:
            return "F" if delta > 0 else "B" if delta < 0 else "-"

        def transition(a, b):
            dist, parent = self.bfs(a)
            if dist.get(b, INF) <= jump_cost(a, b):
                seq = []
                x = b
                while x != a:
                    seq.append(x)
                    x = parent[x]
                prev = a
                for cfg in reversed(seq):
                    lines.append(line({p: step(cfg[0] - prev[0]), q: step(cfg[1] - prev[1])}))
                    prev = cfg
            else:
                dp, dq = b[0] - a[0], b[1] - a[1]
                if max(abs(dp), abs(dq) + 2) <= max(abs(dp) + 2, abs(dq)):
                    off, on, d_off, d_on = q, p, dq, dp
                else:
                    off, on, d_off, d_on = p, q, dp, dq
                total = max(abs(d_off) + 2, abs(d_on))
                for t in range(total):
                    instr = {}
                    if t == 0 or t == total - 1:
                        instr[off] = "T"
                    elif t <= abs(d_off):
                        instr[off] = step(d_off)
                    if t < abs(d_on):
                        instr[on] = step(d_on)
                    lines.append(line(instr))

        cfgs = [self.cfgs[i] for i in path]
        first = cfgs[0]
        if all(self.on):
            transition(self.start_cfg, first)
        else:
            dp, dq = first[0] - self.start_cfg[0], first[1] - self.start_cfg[1]
            for t in range(max(abs(dp), abs(dq))):
                lines.append(line({p: step(dp) if t < abs(dp) else "-", q: step(dq) if t < abs(dq) else "-"}))
            lines.append(line({k: "T" for k, is_on in zip((p, q), self.on) if not is_on}))
        for a, b in zip(cfgs, cfgs[1:]):
            transition(a, b)
        return lines


# ---------------------------------------------------------------------------------------------
# simulation helpers
# ---------------------------------------------------------------------------------------------
def pattern_sets(r: int, cells: list[tuple[int, int]]):
    cell_set = set(cells)
    empty = parse(render(r).split("\n"))
    halo = {(i + di, j + dj) for i, j in cells for di, dj in DIRECTIONS.values()}
    halo = {c for c in halo if c not in cell_set and empty[c[0]][c[1]] == "O"}
    return cell_set, halo


def simulate(r: int, cells: set, halo: set, program: list[list[str]]):
    """Returns (first tick at which a pattern cell holds matter, ticks at which the arm submitted)."""
    fab = Fabricator(r)
    first_paint = None
    submissions = []
    for t, line in enumerate(program):
        grid = fab.tick(line)
        if first_paint is None and any(grid[i][j] == "M" for i, j in cells):
            first_paint = t
        if all(grid[i][j] == "M" for i, j in cells) and not any(in_bounds(grid, i, j) and grid[i][j] == "M" for i, j in halo):
            for i, j in cells:
                grid[i][j] = "O"
            submissions.append(t)
    return first_paint, submissions


def reversed_lines(lines: list[list[str]]) -> list[list[str]]:
    return [[REVERSE[x] for x in line] for line in reversed(lines)]


def assemble(r: int, cells: set, halo: set, k: int, single_pass: list[list[str]]) -> list[list[str]] | None:
    """Expand one pass into a K-pass program (alternating forwards / backwards replay of the part
    after the first painted cell), cut after the K-th submission."""
    first, subs = simulate(r, cells, halo, single_pass)
    if not subs:
        return None
    single_pass = single_pass[: subs[0] + 1]
    core = single_pass[first + 1 :]
    program = list(single_pass)
    boundaries = []
    for p in range(1, k):
        boundaries.append(len(program))
        program.append(IDLE)
        program.extend(core if p % 2 == 0 else reversed_lines(core))
    _, subs = simulate(r, cells, halo, program)
    if len(subs) < k:
        return None
    program = program[: subs[k - 1] + 1]
    # drop idle ticks that turn out to be unnecessary
    for b in reversed(boundaries):
        if b < len(program):
            trial = program[:b] + program[b + 1 :]
            _, subs = simulate(r, cells, halo, trial)
            if len(subs) >= k:
                program = trial[: subs[k - 1] + 1]
    return program


# ---------------------------------------------------------------------------------------------
# strategies
# ---------------------------------------------------------------------------------------------
def single_cursor_pass(r, cells, halo, k, p, q, starts):
    planner = Planner(Cursor(r, p, q), sorted(cells), halo, k)
    return planner.program(planner.best_path(starts))


def painter_pass(r, cells, halo, emitters, starts, heuristic="cursor", seed=0, lookahead=0,
                 prefix=None, pos=None, on=None, missing=None, extra=(), width=1, joint=False):
    """One pass by the painter (greedy, or beam search when width > 1), optionally continuing a
    prefix program from a given emitter state with only `missing` cells left; whatever the painter
    cannot reach is done by one cursor."""
    painter = Painter(r, cells, halo, emitters, extra, joint)
    lines = list(prefix) if prefix else []
    if pos is not None:
        painter.pos.update({k: pos[k] for k in emitters if k in pos})
        painter.on.update({k: on[k] for k in emitters if k in on})
    if width > 1:
        more, missing = painter.beam(width, max_ticks=3 * len(cells) + 6 * r, heuristic=heuristic, seed=seed, missing=missing)
        lines += more
    if width <= 1 or missing:
        more, missing = painter.run(max_stuck=2 * r + 2, heuristic=heuristic, seed=seed, lookahead=lookahead, missing=missing)
        lines += more
    if missing:
        a, b = painter.cursors[0]
        off_line = ["-"] * 6
        for e in painter.E:
            if e != a and painter.on[e]:
                off_line[e - 1] = "T"
                painter.on[e] = False
        if "T" in off_line:
            lines.append(off_line)
        planner = Planner(Cursor(r, a, b), sorted(missing), halo, 1,
                          start_cfg=(painter.offset(a), painter.offset(b)), on=(painter.on[a], False))
        lines += planner.program(planner.best_path(starts))
    return lines


def solve_board(r: int, pattern: Grid, k: int, pairs=PAIRS, emitter_sets=EMITTER_SETS, starts: int = 8,
                report: dict | None = None, seeds: int = 1, lookahead_top: int = 0, sweeps: bool = False,
                shorten_top: int = 0, shorten_budget: float = 2.0, extra_seeds: int = 0,
                beam_width: int = 0, beam_extra: bool = False, joint_width: int = 0, joint_seeds: int = 1) -> list[list[str]]:
    """Try every strategy variant and keep the shortest verified program.

    seeds: number of random tie-break seeds per painter variant.
    lookahead_top: re-run this many of the best painter variants with a one-tick lookahead.
    sweeps: also try the line-sweep strategy (sweep.py) with the painter finishing the leftovers.
    shorten_top: run the local search of shorten.py on this many of the best passes."""
    cells_list = [(i, j) for i, j, _ in find_all(pattern, "M")]
    cells, halo = pattern_sets(r, cells_list)

    passes: dict[str, list[list[str]]] = {}
    candidates: dict[str, list[list[str]]] = {}

    def consider(name: str, single_pass: list[list[str]]) -> int | None:
        prog = assemble(r, cells, halo, k, single_pass)
        if prog is None:
            return None
        passes[name] = single_pass
        candidates[name] = prog
        return len(prog)

    for p, q in pairs:
        consider(f"cursor{p}{q}", single_cursor_pass(r, cells, halo, k, p, q, starts))
    variants = []
    for emitters in emitter_sets:
        for heuristic in ("cursor", "emitter"):
            for seed in range(seeds):
                name = f"painter{''.join(map(str, emitters))}-{heuristic[0]}{seed}"
                length = consider(name, painter_pass(r, cells, halo, emitters, starts, heuristic, seed))
                if length is not None:
                    variants.append((length, emitters, heuristic, seed))
    variants.sort()
    for _length, emitters, heuristic, seed in variants[:lookahead_top]:
        consider(f"painter{''.join(map(str, emitters))}-{heuristic[0]}{seed}L",
                 painter_pass(r, cells, halo, emitters, starts, heuristic, seed, lookahead=1))
    for emitters in emitter_sets:
        for heuristic in ("cursor", "emitter"):
            for seed in range(extra_seeds):
                consider(f"painter{''.join(map(str, emitters))}-{heuristic[0]}{seed}X",
                         painter_pass(r, cells, halo, emitters, starts, heuristic, seed, extra=third_family(emitters)))
    if beam_width > 1:
        for emitters in emitter_sets:
            for heuristic in ("cursor", "emitter"):
                consider(f"painter{''.join(map(str, emitters))}-{heuristic[0]}b{beam_width}",
                         painter_pass(r, cells, halo, emitters, starts, heuristic, 0, width=beam_width))
                if beam_extra:
                    consider(f"painter{''.join(map(str, emitters))}-{heuristic[0]}b{beam_width}X",
                             painter_pass(r, cells, halo, emitters, starts, heuristic, 0, width=beam_width,
                                          extra=third_family(emitters)))
    if joint_width > 0:  # all six emitters searched jointly (beam search, or greedy for width 1)
        for emitters in emitter_sets:
            for heuristic in ("cursor", "emitter"):
                for seed in range(joint_seeds):
                    consider(f"painter{''.join(map(str, emitters))}-{heuristic[0]}j{joint_width}s{seed}",
                             painter_pass(r, cells, halo, emitters, starts, heuristic, seed, width=joint_width,
                                          extra=third_family(emitters), joint=True))
    if sweeps:
        for fill, cutters in SWEEP_CONFIGS:
            for direction in (1, -1):
                result = sweep_pass(r, cells, halo, fill, cutters, direction)
                if result is None:
                    continue
                prefix, pos, on, leftover = result
                emitters = fill + cutters[:2]
                if len(cutters) > 2:  # the painter drives four emitters: switch the extra cutters off
                    off_line = ["-"] * 6
                    for c in cutters[2:]:
                        if on[c]:
                            off_line[c - 1] = "T"
                    if "T" in off_line:
                        prefix = prefix + [off_line]
                for heuristic in ("cursor", "emitter"):
                    name = f"sweep{''.join(map(str, fill))}c{''.join(map(str, cutters))}{'+' if direction > 0 else '-'}{heuristic[0]}"
                    consider(name, painter_pass(r, cells, halo, emitters, starts, heuristic, 0,
                                                prefix=prefix, pos=pos, on=on, missing=leftover))

    # local search on the best few passes: delete / merge / shift lines while the pass stays valid
    if shorten_top:
        ranked = sorted(candidates, key=lambda n: len(candidates[n]))[:shorten_top]
        beams = Beams(r, ALL_EMITTERS)
        for name in ranked:
            shorter = shorten(r, cells, halo, passes[name], budget=shorten_budget, beams=beams)
            if len(shorter) < len(passes[name]):
                consider(name + "S", shorter)

    name, best = min(candidates.items(), key=lambda item: len(item[1]))
    if report is not None:
        report.update({n: len(prog) for n, prog in candidates.items()})
        report["best"] = name
    submitted = count_submissions(r, pattern, best)
    assert submitted == k, f"generated program submits {submitted} patterns instead of {k}"
    return best


def solve(text: str) -> str:
    paragraphs = blocks(text)
    n = int(paragraphs[0][0])
    paragraphs[0] = paragraphs[0][1:]

    out = []
    total = 0
    t0 = time.time()
    for b, lines in enumerate(paragraphs[:n]):
        r, height, _width, k = map(int, lines[0].split())
        pattern = parse(lines[1 : 1 + height])
        m = sum(row.count("M") for row in pattern)
        pairs = PAIRS if m <= 60 else PAIRS[:4] if m <= 150 else PAIRS[:2]
        starts = 12 if m <= 60 else 6 if m <= 150 else 3
        report: dict = {}
        seeds = 4 if m <= 60 else 3 if m <= 150 else 2
        program = solve_board(r, pattern, k, pairs, EMITTER_SETS, starts, report, seeds=seeds, lookahead_top=2,
                              sweeps=True, shorten_top=2, shorten_budget=1.5, extra_seeds=2 if m <= 150 else 1)
        total += len(program)
        out.append("\n".join(" ".join(line) for line in program) + "\n\n")
        print(f"  board {b + 1}/{n}: r={r} cells={m} K={k} -> {len(program)} lines by {report['best']}"
              f"   (total {total}, {time.time() - t0:.0f}s)", file=sys.stderr)
    print(f"  score (total lines): {total}", file=sys.stderr)
    return "".join(out)


if __name__ == "__main__":
    run_level(6, solve)
