"""Level 4 - run each program on an empty board and print the final board (see fabricator.py)."""
from ccc import blocks, run_level
from fabricator import Fabricator, parse_program
from hexboard import unparse


def solve(text: str) -> str:
    paragraphs = blocks(text)
    n = int(paragraphs[0][0])
    paragraphs[0] = paragraphs[0][1:]  # the first paragraph starts with N

    out = []
    for lines in paragraphs[:n]:
        r, steps = int(lines[0]), int(lines[1])
        program = parse_program(lines[2 : 2 + steps])
        out.append(unparse(Fabricator(r).run(program)) + "\n\n")
    return "".join(out)


if __name__ == "__main__":
    run_level(4, solve)
