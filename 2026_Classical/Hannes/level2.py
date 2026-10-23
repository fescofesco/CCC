"""Level 2 - fire each emitter ('1'-'6' on the border) across the board.

The beam travels in the emitter's direction and turns every empty cell 'O'
it passes into matter 'M' until it reaches anything that is not an empty cell.
"""
from ccc import run_level
from hexboard import Grid, emitters, ray, read_boards, unparse


def fire(grid: Grid) -> Grid:
    for row, col, direction in emitters(grid):
        for r, c in ray(grid, row, col, direction, passable="O"):
            grid[r][c] = "M"
    return grid


def solve(text: str) -> str:
    return "".join(unparse(fire(grid)) + "\n\n" for _radius, grid in read_boards(text))


if __name__ == "__main__":
    run_level(2, solve)
