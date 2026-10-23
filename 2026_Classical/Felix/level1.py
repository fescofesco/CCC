"""Level 1 - Nano Fabricator: draw the hexagonal board for each radius.

For a radius r the board has 2r+1 rows and is 4r+1 characters wide.
Row i has d = |i - r| dashes of indentation on each side and 2r+1-d symbols
joined by '-'. The top and bottom rows are all '*'; every other row is a '*',
then 'O' cells, then a '*'.

Usage: python level1.py            (processes every in_level-1_*.txt in ../Input/level1)
"""
from pathlib import Path

INPUT_DIR = Path(__file__).resolve().parent.parent / "Input" / "level1"
OUTPUT_DIR = Path(__file__).resolve().parent / "Outputs" / "level1"


def board(r: int) -> str:
    rows = []
    for i in range(2 * r + 1):
        d = abs(i - r)
        n = 2 * r + 1 - d
        symbols = ["*"] * n if d == r else ["*"] + ["O"] * (n - 2) + ["*"]
        rows.append("-" * d + "-".join(symbols) + "-" * d)
    return "\n".join(rows)


def solve(text: str) -> str:
    numbers = [int(x) for x in text.split()]
    radii = numbers[1 : 1 + numbers[0]]
    return "".join(board(r) + "\n\n" for r in radii)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for in_file in sorted(INPUT_DIR.glob("in_level-1_*.txt")):
        out_file = OUTPUT_DIR / in_file.name.replace("in_", "out_", 1)
        out_file.write_text(solve(in_file.read_text()), newline="\n")
        print(f"{in_file.name} -> {out_file.relative_to(OUTPUT_DIR.parent.parent)}")

    expected = INPUT_DIR / "out_level-1_0-example.txt"
    produced = OUTPUT_DIR / "out_level-1_0-example.txt"
    if expected.exists():
        ok = expected.read_bytes().replace(b"\r\n", b"\n") == produced.read_bytes()
        print("example check:", "PASS" if ok else "FAIL")


if __name__ == "__main__":
    main()
