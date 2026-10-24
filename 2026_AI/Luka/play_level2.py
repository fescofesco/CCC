"""
play_level2.py - plays a Colony: One scene as CYAN, turn by turn.

    python play_level2.py "kb5 Pe2 Kh2"            (uppercase = you/CYAN, lowercase = MAGENTA)
    python play_level2.py "kb5 Pe2 Kh2" --round 3   (if the scene doesn't start at round 1)

After each of your turns, type where MAGENTA's Kernel ended up (e.g. c4),
or the whole position again (e.g. "kc4 Pe2 Kf4") if more changed.
"""
import sys

from colony2 import CY, MG, KER, Game, Solver, describe, parse, render, tile

board = parse(sys.argv[1])
rnd = int(sys.argv[sys.argv.index("--round") + 1]) if "--round" in sys.argv else 1
mr, solver = 0, Solver()

while True:
    print(f"\n--- round {rnd}, your turn ---\n{render(board, mr)}")
    acts, n = solver.best_turn(board, mr, rnd)
    if not acts:
        sys.exit("No forced win found from here. Send the position to Claude.")
    print(f"\nPLAY:  {describe(acts)}      (forced win within {n} of your turns)")
    after = board
    for a in acts:
        after = next(b for x, b, w in Game.actions(after, CY, mr) if x == a)
    w, board, mr, rnd = Game.end_of_turn(after, CY, mr, rnd)
    if w == CY or any(a[3] == "takes the KERNEL" for a in acts):
        sys.exit("\n*** That wins the scene. ***")

    replies = Game.turns(board, MG, mr)
    while True:
        text = input("\nMAGENTA moved. Its Kernel is now on (tile, or full position): ").strip()
        try:
            if len(text.split()) > 1:
                new = parse(text); break
            dest = tile(text)
            options = {tuple(sorted(b.items())): b for a, b, w2 in replies if b.get(dest) == (MG, KER)}
            if len(options) == 1:
                new = next(iter(options.values())); break
            if not options:
                print("MAGENTA can't get there from this position - check the tile or type the full position.")
            else:
                print("Several things could have happened - type the full position, e.g. \"kc4 Pe2 Kf4\".")
        except ValueError as e:
            print(e)
    w, board, mr, rnd = Game.end_of_turn(new, MG, mr, rnd)
    if w is not None:
        sys.exit("\n*** You win the scene. ***" if w == CY else "\nMAGENTA won - send the position to Claude.")
