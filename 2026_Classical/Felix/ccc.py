"""Shared helpers for the Cloudflight Coding Contest 2026, Classical track.

Folder layout, relative to this file:
    ../Input/level<N>/in_level-<N>_*.txt             inputs shared by the whole team
    ../Input/level<N>/out_level-<N>_0-example.txt    expected example output
    ./Outputs/level<N>/out_level-<N>_*.txt           outputs produced by level<N>.py

A level script only needs a solve(text) -> str function and a call to run_level:

    from ccc import blocks, run_level

    def solve(text: str) -> str:
        ...

    if __name__ == "__main__":
        run_level(3, solve)

run_level processes every input file of that level, writes the outputs, and
compares the example output against the expected file shipped in the zip.

Adding a new level from its downloaded zip:
    python ccc.py extract C:/Users/scope/Downloads/level-3.zip
"""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from typing import Callable

FELIX_DIR = Path(__file__).resolve().parent
TRACK_DIR = FELIX_DIR.parent
INPUT_ROOT = TRACK_DIR / "Input"
OUTPUT_ROOT = FELIX_DIR / "Outputs"


def input_dir(level: int) -> Path:
    return INPUT_ROOT / f"level{level}"


def output_dir(level: int) -> Path:
    return OUTPUT_ROOT / f"level{level}"


def read_text(path: Path) -> str:
    """Read a file as text with Unix newlines, regardless of how git checked it out."""
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def blocks(text: str) -> list[list[str]]:
    """Split text into blank-line separated paragraphs, each returned as a list of lines."""
    return [p.split("\n") for p in text.strip().split("\n\n") if p.strip()]


def run_level(level: int, solve: Callable[[str], str]) -> None:
    """Run solve() over every input file of a level and write the outputs."""
    inputs = sorted(input_dir(level).glob(f"in_level-{level}_*.txt"))
    if not inputs:
        sys.exit(f"No input files found in {input_dir(level)}")
    out_dir = output_dir(level)
    out_dir.mkdir(parents=True, exist_ok=True)

    for in_file in inputs:
        result = solve(read_text(in_file))
        out_file = out_dir / in_file.name.replace("in_", "out_", 1)
        out_file.write_text(result, encoding="utf-8", newline="\n")

        status = ""
        expected_file = in_file.with_name(out_file.name)
        if expected_file.exists():
            status = "  PASS" if read_text(expected_file) == result else "  FAIL: differs from expected"
        print(f"{in_file.name} -> Outputs/level{level}/{out_file.name}{status}")


def extract_level(zip_path: str | Path, level: int | None = None) -> int:
    """Extract a level zip into the shared Input folder. The level number is read from the file name."""
    zip_path = Path(zip_path)
    if level is None:
        match = re.search(r"level[-_ ]?(\d+)", zip_path.stem, re.IGNORECASE)
        if not match:
            sys.exit(f"Cannot read the level number from '{zip_path.name}'. Pass it explicitly.")
        level = int(match.group(1))

    target = input_dir(level)
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        for info in archive.infolist():
            name = Path(info.filename).name  # flatten: only the file name, never a path
            if info.is_dir() or not name:
                continue
            (target / name).write_bytes(archive.read(info))
            print(f"  {name}")
    print(f"Extracted {zip_path.name} into {target}")
    return level


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) >= 2 and args[0] == "extract":
        extract_level(args[1], int(args[2]) if len(args) > 2 else None)
    else:
        print(__doc__)
