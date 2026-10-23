"""Level 3 - Colony: One. Build a hand-weighted ONNX policy/value evaluator.

No training: the referee wraps the model in its own MCTS (60 sims/action in
level 3), so the model only has to rank positions and moves sensibly.

Value head  = tanh( <obs, W_val> / SCALE ):
  material difference (own minus enemy, canonical planes) plus kernel
  centrality (endgame rule: more central ring wins) and a mild centre bias.
Policy head = from_score[from] + to_score[to], flattened to 4096 logits:
  to-square holding an enemy piece gets a capture bonus (kernel >> rest),
  central to-squares get a small bias, moving non-kernel pieces slightly
  preferred. The referee softmaxes legal logits only.

Graph ops used: Flatten, Gemm, Unsqueeze, Add, Squeeze, Tanh - all on the
validator allow-list; shapes/axes are baked-in constants. Opset 17.

Usage: python build_model.py  -> writes model.onnx next to this file.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper

HERE = Path(__file__).resolve().parent
OUT = HERE / "model.onnx"

N = 8
NUM_SQ = 64
NUM_PLANES = 16
FLAT = NUM_PLANES * NUM_SQ  # 1024

# plane indices (canonical: 0-5 own, 6-11 enemy; PieceType declaration order)
PING, DAEMON, EXPLOIT, TRACE, ICE, KERNEL = range(6)
ENEMY = 6  # offset
MAGENTA_PLANE = 15

MATERIAL = {PING: 15.0, DAEMON: 45.0, EXPLOIT: 25.0, TRACE: 30.0, ICE: 50.0}
KERNEL_RING_BONUS = [0.0, 4.0, 9.0, 12.0]  # by ring 0 (edge) .. 3 (centre 2x2)
PIECE_RING_BONUS = 0.3
VALUE_SCALE = 1.0 / 120.0

CAPTURE_LOGIT = {PING: 2.0, DAEMON: 3.6, EXPLOIT: 2.5, TRACE: 3.0,
                 ICE: 4.0, KERNEL: 8.0}
TO_CENTER_LOGIT = 0.25
FROM_PIECE_LOGIT = {PING: 0.4, DAEMON: 0.4, EXPLOIT: 0.5, TRACE: 0.4,
                    ICE: 0.4, KERNEL: 0.0}


def ring(sq: int) -> int:
    r, c = divmod(sq, N)
    return min(r, N - 1 - r, c, N - 1 - c)


def build_weights() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    w_val = np.zeros(FLAT, dtype=np.float32)
    for sq in range(NUM_SQ):
        rg = ring(sq)
        for p, mat in MATERIAL.items():
            w_val[p * NUM_SQ + sq] = mat + PIECE_RING_BONUS * rg
            w_val[(ENEMY + p) * NUM_SQ + sq] = -(mat + PIECE_RING_BONUS * rg)
        w_val[KERNEL * NUM_SQ + sq] = KERNEL_RING_BONUS[rg]
        w_val[(ENEMY + KERNEL) * NUM_SQ + sq] = -KERNEL_RING_BONUS[rg]
        # Magenta wins every tiebreak: tiny nudge when we are Magenta.
        w_val[MAGENTA_PLANE * NUM_SQ + sq] = 2.0 / NUM_SQ
    w_val *= VALUE_SCALE

    w_to = np.zeros((FLAT, NUM_SQ), dtype=np.float32)
    b_to = np.array([TO_CENTER_LOGIT * ring(j) for j in range(NUM_SQ)],
                    dtype=np.float32)
    for sq in range(NUM_SQ):
        for p, logit in CAPTURE_LOGIT.items():
            w_to[(ENEMY + p) * NUM_SQ + sq, sq] = logit

    w_from = np.zeros((FLAT, NUM_SQ), dtype=np.float32)
    b_from = np.zeros(NUM_SQ, dtype=np.float32)
    for sq in range(NUM_SQ):
        for p, logit in FROM_PIECE_LOGIT.items():
            w_from[p * NUM_SQ + sq, sq] = logit

    return w_val.reshape(FLAT, 1), w_from, b_from, w_to, b_to


def build_model() -> onnx.ModelProto:
    w_val, w_from, b_from, w_to, b_to = build_weights()

    inits = [
        numpy_helper.from_array(w_from, "W_from"),
        numpy_helper.from_array(b_from, "b_from"),
        numpy_helper.from_array(w_to, "W_to"),
        numpy_helper.from_array(b_to, "b_to"),
        numpy_helper.from_array(w_val, "W_val"),
        numpy_helper.from_array(np.zeros(1, dtype=np.float32), "b_val"),
        numpy_helper.from_array(np.array([2], dtype=np.int64), "ax2"),
        numpy_helper.from_array(np.array([1], dtype=np.int64), "ax1"),
    ]

    nodes = [
        helper.make_node("Flatten", ["observation"], ["flat"], axis=1),
        helper.make_node("Gemm", ["flat", "W_from", "b_from"], ["from_sc"]),
        helper.make_node("Gemm", ["flat", "W_to", "b_to"], ["to_sc"]),
        helper.make_node("Unsqueeze", ["from_sc", "ax2"], ["from_3d"]),
        helper.make_node("Unsqueeze", ["to_sc", "ax1"], ["to_3d"]),
        helper.make_node("Add", ["from_3d", "to_3d"], ["pol_3d"]),
        helper.make_node("Flatten", ["pol_3d"], ["policy"], axis=1),
        helper.make_node("Gemm", ["flat", "W_val", "b_val"], ["val_2d"]),
        helper.make_node("Squeeze", ["val_2d", "ax1"], ["val_1d"]),
        helper.make_node("Tanh", ["val_1d"], ["value"]),
    ]

    graph = helper.make_graph(
        nodes,
        "colony_one_handcrafted",
        inputs=[helper.make_tensor_value_info(
            "observation", TensorProto.FLOAT, ["batch", NUM_PLANES, N, N])],
        outputs=[
            helper.make_tensor_value_info(
                "policy", TensorProto.FLOAT, ["batch", NUM_SQ * NUM_SQ]),
            helper.make_tensor_value_info(
                "value", TensorProto.FLOAT, ["batch"]),
        ],
        initializer=inits,
    )
    model = helper.make_model(
        graph, opset_imports=[helper.make_opsetid("", 17)])
    model.ir_version = 8
    onnx.checker.check_model(model)
    return model


if __name__ == "__main__":
    model = build_model()
    onnx.save(model, OUT)
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.1f} KiB)")
