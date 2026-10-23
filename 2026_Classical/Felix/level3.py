"""Level 3 - all emitters fire at once at half power.

Beams pass through empty cells 'O' and matter 'M' and stop at the border or
another emitter. A cell hit by exactly two beams becomes matter; a cell hit by
three or more beams loses its matter; cells hit by fewer than two are unchanged.
"""
from collections import Counter

from ccc import run_level
from hexboard import Grid, emitters, ray, read_boards, unparse


def simulate(grid: Grid) -> Grid:
    hits: Counter[tuple[int, int]] = Counter()
    for row, col, direction in emitters(grid):
        hits.update(ray(grid, row, col, direction, passable="OM"))
    for (row, col), n in hits.items():
        if n == 2:
            grid[row][col] = "M"
        elif n >= 3:
            grid[row][col] = "O"
    return grid


def solve(text: str) -> str:
    return "".join(unparse(simulate(grid)) + "\n\n" for _radius, grid in read_boards(text))


if __name__ == "__main__":
    run_level(3, solve)
