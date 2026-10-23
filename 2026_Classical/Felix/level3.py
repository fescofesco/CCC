"""Level 3 - all emitters fire at once at half power.

Beams pass through empty cells 'O' and matter 'M' and stop at the border or
another emitter. A cell hit by exactly two beams becomes matter; a cell hit by
three or more beams loses its matter; cells hit by fewer than two are unchanged.
"""
from ccc import run_level
from hexboard import emitters, interfere, read_boards, unparse


def solve(text: str) -> str:
    return "".join(unparse(interfere(grid, emitters(grid))) + "\n\n" for _radius, grid in read_boards(text))


if __name__ == "__main__":
    run_level(3, solve)
