"""Level 4 - six emitters ride on a rail along the border.

Emitter k always fires in direction k (1=E, 2=SE, 3=SW, 4=W, 5=NW, 6=NE) and
starts inactive in its own corner. Each tick one instruction line with one
instruction per emitter is applied simultaneously: F moves the emitter one
border cell clockwise, B one counterclockwise, T toggles it on/off, - does
nothing. Then every active emitter fires and matter is created and destroyed
with the level 3 rule. The board starts empty.
"""
from ccc import blocks, run_level
from hexboard import CORNER_INDEX, DIRECTIONS, Grid, border_ring, interfere, parse, render, unparse

EMITTERS = range(1, 7)


def run_program(r: int, program: list[list[str]]) -> Grid:
    grid = parse(render(r).split("\n"))
    ring = border_ring(r)
    position = {k: CORNER_INDEX[k] * r for k in EMITTERS}
    active = {k: False for k in EMITTERS}

    for line in program:
        for k, instruction in zip(EMITTERS, line):
            if instruction == "F":
                position[k] = (position[k] + 1) % len(ring)
            elif instruction == "B":
                position[k] = (position[k] - 1) % len(ring)
            elif instruction == "T":
                active[k] = not active[k]
            elif instruction != "-":
                raise ValueError(f"unknown instruction {instruction!r}")
        sources = [(*ring[position[k]], DIRECTIONS[k]) for k in EMITTERS if active[k]]
        interfere(grid, sources)
    return grid


def solve(text: str) -> str:
    paragraphs = blocks(text)
    n = int(paragraphs[0][0])
    paragraphs[0] = paragraphs[0][1:]  # the first paragraph starts with N

    out = []
    for lines in paragraphs[:n]:
        r, steps = int(lines[0]), int(lines[1])
        program = [line.split() for line in lines[2 : 2 + steps]]
        out.append(unparse(run_program(r, program)) + "\n\n")
    return "".join(out)


if __name__ == "__main__":
    run_level(4, solve)
