"""Generate AlphaZero-style self-play data on the level 4 scene.

Each action: run the referee MCTS (100 sims) with the current best ONNX
model, record (observation, root visit distribution, side to move), then
play by the referee's own sampling schedule. After the game every position
gets the outcome z from its side-to-move perspective.

Usage: python selfplay.py WORKER_ID N_GAMES OUT_DIR [MODEL]
Writes OUT_DIR/worker_{id}.npz with:
  obs      (M,16,8,8) float32
  pol_idx  concatenated int32 action indices
  pol_cnt  concatenated float32 visit counts
  pol_off  (M+1,) int64 offsets into pol_idx/pol_cnt
  z        (M,) float32 outcome for side to move
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


def main() -> None:
    worker = int(sys.argv[1])
    n_games = int(sys.argv[2])
    out_dir = Path(sys.argv[3])
    model = sys.argv[4] if len(sys.argv) > 4 else str(HERE / "model_v7.onnx")
    out_dir.mkdir(parents=True, exist_ok=True)

    evaluator = OnnxEvaluator(model)
    cfg = mcts.MCTSConfig(simulations=100)
    rng = np.random.default_rng(97000 + worker)

    obs_l, idx_l, cnt_l, team_l, game_id_l = [], [], [], [], []
    results = {}
    t0 = time.time()
    for g in range(n_games):
        env = ColonyOneEnv(seed=int(rng.integers(1 << 31)),
                           scene=SCENE.copy())
        env.reset()
        while not env.terminated:
            team = env.current_team
            root = mcts.run(env.board, team, env.actions_left,
                            env.round_number, evaluator, cfg, rng=rng)
            indices, counts = mcts.visit_distribution(root)
            obs_l.append(env.observation())
            idx_l.append(np.asarray(indices, np.int32))
            cnt_l.append(np.asarray(counts, np.float32))
            team_l.append(team)
            game_id_l.append(g)
            temp = mcts.warmup_temperature(
                mcts.move_number(team, env.actions_left, env.round_number),
                cfg.warmup_temperatures, cfg.warmup_step_actions)
            action = mcts.select_action_index(root, temp, rng=rng)
            env.step(action)
        results[g] = env.winner
        if (g + 1) % 10 == 0:
            print(f"[w{worker}] {g + 1}/{n_games} games, "
                  f"{len(obs_l)} samples, {time.time() - t0:.0f}s",
                  flush=True)

    z = np.array([1.0 if results[gi] == t else -1.0
                  for gi, t in zip(game_id_l, team_l)], np.float32)
    off = np.zeros(len(idx_l) + 1, np.int64)
    np.cumsum([len(a) for a in idx_l], out=off[1:])
    np.savez_compressed(
        out_dir / f"worker_{worker}.npz",
        obs=np.stack(obs_l).astype(np.float32),
        pol_idx=np.concatenate(idx_l),
        pol_cnt=np.concatenate(cnt_l),
        pol_off=off,
        z=z,
    )
    print(f"[w{worker}] DONE {len(obs_l)} samples "
          f"({time.time() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
