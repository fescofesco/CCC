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


def ray(grid: Grid, row: int, col: int, direction: tuple[int, int], passable: str = "O"):
    """Yield the (row, col) cells from the start position in `direction`, as long as each cell's
    character is in `passable`. The start position itself is not yielded."""
    d_row, d_col = direction
    row, col = row + d_row, col + d_col
    while in_bounds(grid, row, col) and grid[row][col] in passable:
        yield row, col
        row, col = row + d_row, col + d_col


def emitters(grid: Grid) -> list[tuple[int, int, tuple[int, int]]]:
    """Every emitter on the board as (row, col, direction)."""
    return [(i, j, DIRECTIONS[int(c)]) for i, j, c in find_all(grid, "123456")]


def read_boards(text: str) -> list[tuple[int, Grid]]:
    """Parse the level 2+ input format: N, then N boards each made of an 'r rows cols' header line
    followed by the board lines, with blank lines between boards. Returns [(radius, grid), ...]."""
    from ccc import blocks

    paragraphs = blocks(text)
    n = int(paragraphs[0][0])
    paragraphs[0] = paragraphs[0][1:]  # the first paragraph starts with N
    boards = []
    for lines in paragraphs[:n]:
        radius, height, _width = map(int, lines[0].split())
        boards.append((radius, parse(lines[1 : 1 + height])))
    return boards
