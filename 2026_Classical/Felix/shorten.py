"""Local search that shortens a level 6 pass without changing what it achieves.

A pass is valid when, replayed from the initial state (all emitters off in
their corners), every state is safe (no halo cell painted, no pattern cell hit
by three or more beams) and the union of painted cells covers the pattern.
The search repeatedly tries to delete a line, merge two neighbouring lines whose
instructions do not clash, or shift one emitter's instruction to a neighbouring
line, keeping every change that leaves the pass valid and not longer.
"""
from __future__ import annotations

import time

from hexboard import CORNER_INDEX
from sweep import Beams, apply_line

ALL_EMITTERS = (1, 2, 3, 4, 5, 6)


def valid_pass(beams: Beams, lines: list[list[str]], P: set, halo: set) -> bool:
    pos = {k: CORNER_INDEX[k] * beams.r for k in beams.E}
    on = {k: False for k in beams.E}
    painted: set = set()
    for line in lines:
        state = apply_line(beams, pos, on, line)
        if state is None:
            return False
        pos, on = state
        cells = beams.painted(pos, on, P, halo)
        if cells is None:
            return False
        painted.update(cells)
    return painted >= P


def shorten(r: int, P: set, halo: set, lines: list[list[str]], budget: float = 2.0,
            beams: Beams | None = None) -> list[list[str]]:
    beams = beams or Beams(r, ALL_EMITTERS)
    lines = [list(line) for line in lines]
    deadline = time.time() + budget
    rounds = 0
    improved = True
    while improved and time.time() < deadline and rounds < 6:
        improved = False
        rounds += 1
        # delete single lines
        t = 0
        while t < len(lines) and time.time() < deadline:
            trial = lines[:t] + lines[t + 1 :]
            if valid_pass(beams, trial, P, halo):
                lines = trial
                improved = True
            else:
                t += 1
        # merge neighbouring lines that use different emitters
        t = 0
        while t < len(lines) - 1 and time.time() < deadline:
            a, b = lines[t], lines[t + 1]
            if all(x == "-" or y == "-" for x, y in zip(a, b)):
                merged = [x if x != "-" else y for x, y in zip(a, b)]
                trial = lines[:t] + [merged] + lines[t + 2 :]
                if valid_pass(beams, trial, P, halo):
                    lines = trial
                    improved = True
                    continue
            t += 1
        # shift one instruction to the previous or next line, then retry deletions next round
        if not improved:
            for t in range(len(lines)):
                if time.time() >= deadline:
                    break
                for e in range(6):
                    ins = lines[t][e]
                    if ins == "-":
                        continue
                    for u in (t - 1, t + 1):
                        if 0 <= u < len(lines) and lines[u][e] == "-":
                            trial = [list(line) for line in lines]
                            trial[t][e] = "-"
                            trial[u][e] = ins
                            if valid_pass(beams, trial, P, halo):
                                # a neutral move: keep it only if it unlocks a deletion
                                for d in (t, u):
                                    shorter = trial[:d] + trial[d + 1 :]
                                    if valid_pass(beams, shorter, P, halo):
                                        lines = shorter
                                        improved = True
                                        break
                                if improved:
                                    break
                    if improved:
                        break
                if improved:
                    break
    return lines
