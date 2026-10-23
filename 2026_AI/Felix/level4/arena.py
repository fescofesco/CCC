"""Arena: pit two ONNX models on the LEVEL 4 scene under referee MCTS.

Usage: python arena.py A.onnx B.onnx [games] [simulations]
Sides alternate; reports A's win rate. Mirrors the tournament settings
(100 simulations/action) by default.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

from colony_one import encoding, mcts
from colony_one.env import ColonyOneEnv
from colony_one.onnx_runner import OnnxEvaluator

HERE = Path(__file__).resolve().parent
SCENE = np.array(json.load(open(HERE / "level-4_scene.json")),
                 dtype=np.float32)


def play(ev_cyan, ev_magenta, seed: int, sims: int) -> tuple[str, int]:
    env = ColonyOneEnv(seed=seed, scene=SCENE.copy())
    env.reset()
    cfg = mcts.MCTSConfig(simulations=sims)
    rng = np.random.default_rng(seed)
    n = 0
    while not env.terminated:
        team = env.current_team
        ev = ev_cyan if team == "CYAN" else ev_magenta
        action = mcts.search_action(
            env.board, team, env.actions_left, env.round_number, ev, cfg,
            rng=rng)
        env.step(encoding.action_index(action, team))
        n += 1
    return env.winner, n


def main() -> None:
    path_a, path_b = Path(sys.argv[1]), Path(sys.argv[2])
    games = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    sims = int(sys.argv[4]) if len(sys.argv) > 4 else 100
    ev_a, ev_b = OnnxEvaluator(path_a), OnnxEvaluator(path_b)
    a_wins = 0
    lengths = []
    t0 = time.time()
    for g in range(games):
        a_is_cyan = g % 2 == 0
        winner, n = play(ev_a if a_is_cyan else ev_b,
                         ev_b if a_is_cyan else ev_a,
                         seed=5000 + g, sims=sims)
        a_won = (winner == "CYAN") == a_is_cyan
        a_wins += a_won
        lengths.append(n)
    dt = time.time() - t0
    print(f"{path_a.name} vs {path_b.name} on LEVEL 4 scene "
          f"({games} games, {sims} sims)")
    print(f"  {path_a.name}: {a_wins} wins ({100 * a_wins / games:.0f}%)")
    print(f"  {path_b.name}: {games - a_wins} wins")
    print(f"  avg length {np.mean(lengths):.1f} actions, "
          f"{dt / games:.2f}s/game")


if __name__ == "__main__":
    main()
