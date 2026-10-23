"""Level 2 - fire each emitter ('1'-'6' on the border) across the board.

The laser travels in the emitter's direction and turns every empty cell 'O'
it passes into matter 'M' until it reaches anything that is not an empty cell.
"""
from ccc import blocks, run_level
from hexboard import DIRECTIONS, Grid, find_all, in_bounds, parse, unparse


def fire(grid: Grid) -> Grid:
    for row, col, digit in find_all(grid, "123456"):
        d_row, d_col = DIRECTIONS[int(digit)]
        row, col = row + d_row, col + d_col
        while in_bounds(grid, row, col) and grid[row][col] == "O":
            grid[row][col] = "M"
            row, col = row + d_row, col + d_col
    return grid


def solve(text: str) -> str:
    paragraphs = blocks(text)
    n = int(paragraphs[0][0])
    paragraphs[0] = paragraphs[0][1:]  # the first paragraph starts with N

    out = []
    for lines in paragraphs[:n]:
        _radius, height, _width = map(int, lines[0].split())
        grid = parse(lines[1 : 1 + height])
        out.append(unparse(fire(grid)) + "\n\n")
    return "".join(out)


if __name__ == "__main__":
    run_level(2, solve)
