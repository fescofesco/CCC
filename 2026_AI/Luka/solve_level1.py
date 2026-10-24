"""
solve_level1.py - Colony: One, Level 1 "In a Pinch".

Copy each scene from the game into SCENES (top row first):
    K P = CYAN (you)    k p = MAGENTA    . = empty
or put each scene in a text file and run:  python solve_level1.py scene1.txt scene2.txt scene3.txt
"""
import sys
from pathlib import Path

from colony import Board, TurnSolver

SCENES = {
    "example (replace with the real scenes)": """
        . . . . . . . .
        . K . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . K
        . . . . . . P .
    """,
}

if __name__ == "__main__":
    scenes = {path: Path(path).read_text() for path in sys.argv[1:]} or SCENES
    for name, text in scenes.items():
        print(f"===== {name} =====")
        print(TurnSolver(Board.from_text(text)).report(), end="\n\n")
