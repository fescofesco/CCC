# 2026 AI Track — Colony: One (Felix)

Team **fehalu** · CCC 2026 AI contest ("Colony: One")

## Levels 1–2 (interactive)

Solved by hand with move-by-move analysis: safe-tile puzzle (L1) and two
win-the-game scenes (L2). Key tricks: Chebyshev-distance safety radii, the
bodyguard rule, and the two-Kernel endgame rule (center ring wins), which
makes a centered Kernel turn the Ping into poisoned bait.

## Level 3 (first ONNX upload)

`level3/build_model.py` hand-writes an ONNX policy/value evaluator with
`onnx.helper` — no training. Material values + Kernel centrality in the
value head, capture/centralize priors in the policy. The referee's MCTS
(60 sims) does the tactics. 35/40 vs the server's GreedyAgent.

## Level 4 (tournament)

Pipeline, each stage gated by `level4/arena.py` (referee-identical matches):

1. **Hand-tuned evaluators v1–v7** (`build_v3.py`): parameterized weights,
   iterated against downloaded loss replays (firewall deaths, Kernel
   exposure, Trace snipes).
2. **Self-play data** (`selfplay.py`): referee MCTS plays the current best
   model vs itself; positions + root visit counts + outcomes recorded.
   ~4,500 games across 4 rounds, 6 parallel workers.
3. **Training** (`train.py`): small CNN (3 conv layers, 64ch) imitates the
   search (CE on visit distribution) and predicts outcomes (MSE).
   net_b beat v7 74%; net_c beat net_b 70% (iteration 2).
4. **Export fixes** (`fold_constants.py`): torch exports Constant nodes the
   contest validator rejects; folded into initializers.
5. **Fusion** (`merge_models.py`): net_c + Luka's hand-coded evaluator
   spliced into one graph (logits added, values averaged).
   58% vs Luka's model alone over 100 games — the deployed submission
   (`kernel76_fusion.onnx`).

Match telemetry lives in `level4/matches/` with `analyze.py`.
Explainer diagram: `level4/kernel76_fusion_explainer.png`.
