"""Level 6 - write a short program that submits each pattern K times (optimization level).

Strategy: with exactly two active beams, matter appears only at their crossing
cell, so a pair of emitters from different direction families acts as a cursor
that writes one cell per tick. Each emitter moves one border cell per tick, so
the cursor makes king moves in the (line of emitter p, line of emitter q)
configuration grid. It must never land on a halo cell (an empty cell touching
the pattern), because that would block the pick-up arm; landing on far cells or
outside the board is harmless. Where the halo is in the way, one emitter is
switched off for the move (2 extra ticks). The pattern cells are ordered into a
short path (nearest neighbour + 2-opt + or-opt), which is walked forwards and
backwards alternately for the K repetitions, with one idle tick in between to
re-create the cell the arm has just removed. Every program is re-simulated with
the level 5 engine before it is written.
"""
from __future__ import annotations

import random
import sys
import time
from collections import deque

from ccc import blocks, run_level
from hexboard import CORNER_INDEX, DIRECTIONS, Grid, border_ring, find_all, parse, ray, render
from level5 import count_submissions

INF = 10**9
PAIRS = [(p, q) for p in (1, 4) for q in (2, 3, 5, 6)] + [(p, q) for p in (2, 5) for q in (3, 6)]
random.seed(42)


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
    def __init__(self, cursor: Cursor, cells: list[tuple[int, int]], halo: set, k: int):
        self.cur = cursor
        self.k = k
        self.cells = cells
        self.cfgs = [cursor.config(c) for c in cells]
        self.forbidden = {cfg for cfg, cell in cursor.cross.items() if cell in halo}
        self.start_cfg = (cursor.start[cursor.p], cursor.start[cursor.q])
        m = len(cells)
        self.D = [[0] * m for _ in range(m)]
        for i, cfg in enumerate(self.cfgs):
            dist, _ = self.bfs(cfg)
            row = self.D[i]
            for j, other in enumerate(self.cfgs):
                row[j] = min(dist.get(other, INF), jump_cost(cfg, other))
        self.setup = [max(abs(c[0] - self.start_cfg[0]), abs(c[1] - self.start_cfg[1])) + 1 for c in self.cfgs]

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
                    if u is None:
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

    # ---- program generation -------------------------------------------------------------
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

        cfgs = [self.cfgs[i] for i in path]

        # setup: move both (inactive) emitters to the first cell, then switch both on
        dp, dq = cfgs[0][0] - self.start_cfg[0], cfgs[0][1] - self.start_cfg[1]
        for t in range(max(abs(dp), abs(dq))):
            lines.append(line({p: step(dp) if t < abs(dp) else "-", q: step(dq) if t < abs(dq) else "-"}))
        lines.append(line({p: "T", q: "T"}))

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

        for pass_no in range(self.k):
            order = cfgs if pass_no % 2 == 0 else cfgs[::-1]
            if pass_no > 0:
                lines.append(["-"] * 6)  # idle tick: re-create the cell the arm just removed
            for a, b in zip(order, order[1:]):
                transition(a, b)
        return lines


def solve_board(r: int, pattern: Grid, k: int, pairs=PAIRS, starts: int = 8) -> list[list[str]]:
    cells = [(i, j) for i, j, _ in find_all(pattern, "M")]
    cell_set = set(cells)
    empty = parse(render(r).split("\n"))
    halo = {(i + di, j + dj) for i, j in cells for di, dj in DIRECTIONS.values()}
    halo = {c for c in halo if c not in cell_set and empty[c[0]][c[1]] == "O"}

    best = None
    for p, q in pairs:
        planner = Planner(Cursor(r, p, q), cells, halo, k)
        path = planner.best_path(starts)
        program = planner.program(path)
        if best is None or len(program) < len(best):
            best = program

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
        program = solve_board(r, pattern, k, pairs, starts)
        total += len(program)
        out.append("\n".join(" ".join(line) for line in program) + "\n\n")
        print(f"  board {b + 1}/{n}: r={r} cells={m} K={k} -> {len(program)} lines   (total {total}, {time.time() - t0:.0f}s)", file=sys.stderr)
    print(f"  score (total lines): {total}", file=sys.stderr)
    return "".join(out)


if __name__ == "__main__":
    run_level(6, solve)
