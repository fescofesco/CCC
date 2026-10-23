"""Level 1 - draw the empty hexagonal board for each radius."""
from ccc import run_level
from hexboard import render


def solve(text: str) -> str:
    numbers = [int(x) for x in text.split()]
    radii = numbers[1 : 1 + numbers[0]]
    return "".join(render(r) + "\n\n" for r in radii)


if __name__ == "__main__":
    run_level(1, solve)
