"""Level 5 - the pick-up arm: count how many times a program produces the given pattern.

Each tick runs as in level 4, then the arm checks the board: if every cell of the
pattern holds matter and no other matter is adjacent to any pattern cell, the
pattern is submitted, which removes its matter from the board.
"""
from ccc import blocks, run_level
from fabricator import Fabricator, parse_program
from hexboard import DIRECTIONS, Grid, find_all, in_bounds, parse


def count_submissions(r: int, pattern: Grid, program: list[list[str]]) -> int:
    cells = {(i, j) for i, j, _ in find_all(pattern, "M")}
    halo = {(i + di, j + dj) for i, j in cells for di, dj in DIRECTIONS.values()} - cells
    if not cells:
        return 0

    fab = Fabricator(r)
    submitted = 0
    for line in program:
        grid = fab.tick(line)
        complete = all(grid[i][j] == "M" for i, j in cells)
        touched = any(in_bounds(grid, i, j) and grid[i][j] == "M" for i, j in halo)
        if complete and not touched:
            for i, j in cells:
                grid[i][j] = "O"
            submitted += 1
    return submitted


def solve(text: str) -> str:
    paragraphs = blocks(text)
    n = int(paragraphs[0][0])
    paragraphs[0] = paragraphs[0][1:]  # the first paragraph starts with N

    out = []
    for lines in paragraphs[:n]:
        r, height, _width = map(int, lines[0].split())
        pattern = parse(lines[1 : 1 + height])
        steps = int(lines[1 + height])
        program = parse_program(lines[2 + height : 2 + height + steps])
        out.append(f"{count_submissions(r, pattern, program)}\n")
    return "".join(out)


if __name__ == "__main__":
    run_level(5, solve)
