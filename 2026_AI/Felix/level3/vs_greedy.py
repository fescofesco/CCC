"""Measure model.onnx vs GreedyAgent under exact Level 3 referee settings.

The model side is driven by the referee MCTS (60 simulations/action, default
noise and warmup temperatures); Greedy plays the published baseline. Sides
alternate across games.

Usage: python vs_greedy.py [games]
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

from colony_one import encoding, mcts
from colony_one.baselines import GreedyAgent
from colony_one.env import ColonyOneEnv
from colony_one.onnx_runner import OnnxEvaluator

MODEL = Path(__file__).resolve().parent / "model.onnx"


def play(evaluator, model_team: str, seed: int) -> tuple[str, int]:
    env = ColonyOneEnv(seed=seed)
    env.reset()
    greedy = GreedyAgent(seed=seed)
    cfg = mcts.MCTSConfig(simulations=60)
    rng = np.random.default_rng(seed)
    actions = 0
    while not env.terminated:
        team = env.current_team
        if team == model_team:
            action = mcts.search_action(
                env.board, team, env.actions_left, env.round_number,
                evaluator, cfg, rng=rng)
        else:
            action = greedy.select(
                env.board, team, env.actions_left, env.round_number)
        env.step(encoding.action_index(action, team))
        actions += 1
    return env.winner, actions


def main() -> None:
    games = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    evaluator = OnnxEvaluator(MODEL)
    wins = 0
    t0 = time.time()
    for g in range(games):
        model_team = "CYAN" if g % 2 == 0 else "MAGENTA"
        winner, n_actions = play(evaluator, model_team, seed=1000 + g)
        won = winner == model_team
        wins += won
        print(f"game {g + 1:>2}: model as {model_team:<7} -> "
              f"{'WIN ' if won else 'loss'} ({winner} after {n_actions} actions)")
    dt = time.time() - t0
    print(f"\nmodel wins {wins}/{games} ({100 * wins / games:.0f}%) "
          f"[{dt / games:.1f} s/game]")


if __name__ == "__main__":
    main()
