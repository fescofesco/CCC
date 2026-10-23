"""FAB-42 itself: six emitters riding the border rail, driven by instruction lines (level 4+).

Emitter k always fires in direction k (1=E, 2=SE, 3=SW, 4=W, 5=NW, 6=NE) and starts
inactive in its own corner. An instruction line holds one instruction per emitter:
F moves it one border cell clockwise, B one counterclockwise, T toggles it on/off,
- does nothing. A tick executes one line for all six emitters at once, then every
active emitter fires and matter is created and destroyed with the level 3 rule.
"""
from __future__ import annotations

from hexboard import CORNER_INDEX, DIRECTIONS, Grid, border_ring, interfere, parse, render

EMITTERS = range(1, 7)


def parse_program(lines: list[str]) -> list[list[str]]:
    return [line.split() for line in lines]


class Fabricator:
    def __init__(self, r: int):
        self.grid: Grid = parse(render(r).split("\n"))
        self.ring = border_ring(r)
        self.position = {k: CORNER_INDEX[k] * r for k in EMITTERS}
        self.active = {k: False for k in EMITTERS}

    def tick(self, line: list[str]) -> Grid:
        """Execute one instruction line, then create and destroy matter. Returns the live grid."""
        for k, instruction in zip(EMITTERS, line):
            if instruction == "F":
                self.position[k] = (self.position[k] + 1) % len(self.ring)
            elif instruction == "B":
                self.position[k] = (self.position[k] - 1) % len(self.ring)
            elif instruction == "T":
                self.active[k] = not self.active[k]
            elif instruction != "-":
                raise ValueError(f"unknown instruction {instruction!r}")
        sources = [(*self.ring[self.position[k]], DIRECTIONS[k]) for k in EMITTERS if self.active[k]]
        return interfere(self.grid, sources)

    def run(self, program: list[list[str]]) -> Grid:
        for line in program:
            self.tick(line)
        return self.grid
