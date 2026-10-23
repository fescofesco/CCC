"""Hexagonal board geometry in the contest's character layout.

A board of radius r has 2r+1 rows and 4r+1 columns. Row i is indented by
d = |i - r| dashes on each side and holds 2r+1-d symbols separated by '-'.
Because of that layout the six neighbours of position (row, col) are:
same row at col +/- 2, and the rows above and below at col +/- 1.
"""
from __future__ import annotations

# Emitter directions as (row step, column step), numbered as in the level 2 statement.
DIRECTIONS: dict[int, tuple[int, int]] = {
    1: (0, 2),    # east
    2: (1, 1),    # south-east
    3: (1, -1),   # south-west
    4: (0, -2),   # west
    5: (-1, -1),  # north-west
    6: (-1, 1),   # north-east
}

Grid = list[list[str]]


def render(r: int) -> str:
    """The empty board of radius r: '*' border, 'O' cells, '-' padding (level 1)."""
    rows = []
    for i in range(2 * r + 1):
        d = abs(i - r)
        n = 2 * r + 1 - d
        symbols = ["*"] * n if d == r else ["*"] + ["O"] * (n - 2) + ["*"]
        rows.append("-" * d + "-".join(symbols) + "-" * d)
    return "\n".join(rows)


def parse(lines: list[str]) -> Grid:
    """Board lines -> mutable grid of characters."""
    return [list(row) for row in lines]


def unparse(grid: Grid) -> str:
    return "\n".join("".join(row) for row in grid)


def in_bounds(grid: Grid, row: int, col: int) -> bool:
    return 0 <= row < len(grid) and 0 <= col < len(grid[row])


def find_all(grid: Grid, chars: str) -> list[tuple[int, int, str]]:
    """Every (row, col, char) whose char is in `chars`, in reading order."""
    return [(i, j, c) for i, line in enumerate(grid) for j, c in enumerate(line) if c in chars]
