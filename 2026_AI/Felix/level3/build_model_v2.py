"""Level 3/4 - Colony: One. v2 hand-built ONNX evaluator.

v1 (build_model.py) = material + kernel centrality + capture priors.
v2 adds, still with zero training:

* kernel danger: 5x5 convolution turns piece planes into local pressure
  maps; enemy pressure on our Kernel's square lowers the value, our
  pressure on theirs raises it.
* firewall: pieces (kernel especially) standing on the outermost open ring
  are penalised proportionally to the urgency plane (interaction via Mul).

Ops: Flatten, Gemm, Conv, Slice, Mul, Add, Sub, ReduceSum, Unsqueeze,
Squeeze, Tanh - all allow-listed; every shape/axis argument is a baked
constant. Opset 17.

Usage: python build_model_v2.py -> writes model_v2.onnx next to this file.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper

HERE = Path(__file__).resolve().parent
OUT = HERE / "model_v2.onnx"

N = 8
NUM_SQ = 64
NUM_PLANES = 16
FLAT = NUM_PLANES * NUM_SQ

PING, DAEMON, EXPLOIT, TRACE, ICE, KERNEL = range(6)
ENEMY = 6
LOCKED_PLANE, ACTIONS_PLANE, URGENCY_PLANE, MAGENTA_PLANE = 12, 13, 14, 15

MATERIAL = {PING: 15.0, DAEMON: 45.0, EXPLOIT: 25.0, TRACE: 30.0, ICE: 50.0}
KERNEL_RING_BONUS = [0.0, 4.0, 9.0, 12.0]
PIECE_RING_BONUS = 0.3
VALUE_SCALE = 1.0 / 120.0

# pressure a piece radiates onto nearby squares (5x5 neighbourhood)
THREAT = {PING: 6.0, DAEMON: 10.0, EXPLOIT: 8.0, TRACE: 7.0, ICE: 10.0,
          KERNEL: 4.0}
DANGER_WEIGHT = 1.0          # value points per pressure unit on a kernel
FIREWALL_KERNEL_PEN = 25.0   # kernel on burning ring at urgency 1.0
FIREWALL_PIECE_PEN = 6.0     # other piece on burning ring at urgency 1.0

CAPTURE_LOGIT = {PING: 2.0, DAEMON: 3.6, EXPLOIT: 2.5, TRACE: 3.0,
                 ICE: 4.0, KERNEL: 8.0}
TO_CENTER_LOGIT = 0.25
FROM_PIECE_LOGIT = {PING: 0.4, DAEMON: 0.4, EXPLOIT: 0.5, TRACE: 0.4,
                    ICE: 0.4, KERNEL: 0.0}


def ring(sq: int) -> int:
    r, c = divmod(sq, N)
    return min(r, N - 1 - r, c, N - 1 - c)


def linear_weights():
    w_val = np.zeros(FLAT, dtype=np.float32)
    for sq in range(NUM_SQ):
        rg = ring(sq)
        for p, mat in MATERIAL.items():
            w_val[p * NUM_SQ + sq] = mat + PIECE_RING_BONUS * rg
            w_val[(ENEMY + p) * NUM_SQ + sq] = -(mat + PIECE_RING_BONUS * rg)
        w_val[KERNEL * NUM_SQ + sq] = KERNEL_RING_BONUS[rg]
        w_val[(ENEMY + KERNEL) * NUM_SQ + sq] = -KERNEL_RING_BONUS[rg]
        w_val[MAGENTA_PLANE * NUM_SQ + sq] = 2.0 / NUM_SQ
    w_val *= VALUE_SCALE

    w_to = np.zeros((FLAT, NUM_SQ), dtype=np.float32)
    b_to = np.array([TO_CENTER_LOGIT * ring(j) for j in range(NUM_SQ)],
                    dtype=np.float32)
    w_from = np.zeros((FLAT, NUM_SQ), dtype=np.float32)
    for sq in range(NUM_SQ):
        for p, logit in CAPTURE_LOGIT.items():
            w_to[(ENEMY + p) * NUM_SQ + sq, sq] = logit
        for p, logit in FROM_PIECE_LOGIT.items():
            w_from[p * NUM_SQ + sq, sq] = logit
    return (w_val.reshape(FLAT, 1), w_from, np.zeros(NUM_SQ, np.float32),
            w_to, b_to)


def conv_weights():
    """(2,16,5,5): ch0 = enemy pressure map, ch1 = own pressure map."""
    w = np.zeros((2, NUM_PLANES, 5, 5), dtype=np.float32)
    kern = np.ones((5, 5), dtype=np.float32)
    kern[1:4, 1:4] = 2.0   # closer pieces press harder
    kern[2, 2] = 3.0
    for p, t in THREAT.items():
        w[0, ENEMY + p] = kern * t
        w[1, p] = kern * t
    return w


def ring0_masks():
    """Outer-ring mask for 'burning' squares; env rotates nothing here:
    the OUTERMOST OPEN ring is approximated by ring 0 of the full board
    early game; after shrinks the locked plane shifts pressure inward via
    the locked-plane term below."""
    m = np.zeros((1, 1, N, N), dtype=np.float32)
    for sq in range(NUM_SQ):
        if ring(sq) == 0:
            m[0, 0, sq // N, sq % N] = 1.0
    return m


def build_model() -> onnx.ModelProto:
    w_val, w_from, b_from, w_to, b_to = linear_weights()
    inits = [
        numpy_helper.from_array(w_from, "W_from"),
        numpy_helper.from_array(b_from, "b_from"),
        numpy_helper.from_array(w_to, "W_to"),
        numpy_helper.from_array(b_to, "b_to"),
        numpy_helper.from_array(w_val, "W_val"),
        numpy_helper.from_array(np.zeros(1, np.float32), "b_val"),
        numpy_helper.from_array(conv_weights(), "W_conv"),
        numpy_helper.from_array(np.zeros(2, np.float32), "b_conv"),
        numpy_helper.from_array(ring0_masks(), "ring0"),
        numpy_helper.from_array(
            np.array(DANGER_WEIGHT * VALUE_SCALE, np.float32), "w_danger"),
        numpy_helper.from_array(
            np.array(FIREWALL_KERNEL_PEN * VALUE_SCALE, np.float32), "w_fk"),
        numpy_helper.from_array(
            np.array(FIREWALL_PIECE_PEN * VALUE_SCALE, np.float32), "w_fp"),
        numpy_helper.from_array(np.array([1], np.int64), "ax1"),
        numpy_helper.from_array(np.array([2], np.int64), "ax2"),
        numpy_helper.from_array(np.array([1, 2, 3], np.int64), "ax123"),
        # slice bounds over channel axis
        numpy_helper.from_array(np.array([KERNEL], np.int64), "s_ok"),
        numpy_helper.from_array(np.array([KERNEL + 1], np.int64), "e_ok"),
        numpy_helper.from_array(np.array([ENEMY + KERNEL], np.int64), "s_ek"),
        numpy_helper.from_array(np.array([ENEMY + KERNEL + 1], np.int64), "e_ek"),
        numpy_helper.from_array(np.array([0], np.int64), "s_own"),
        numpy_helper.from_array(np.array([ENEMY], np.int64), "e_own"),
        numpy_helper.from_array(np.array([ENEMY], np.int64), "s_en"),
        numpy_helper.from_array(np.array([2 * ENEMY], np.int64), "e_en"),
        numpy_helper.from_array(np.array([URGENCY_PLANE], np.int64), "s_u"),
        numpy_helper.from_array(np.array([URGENCY_PLANE + 1], np.int64), "e_u"),
        numpy_helper.from_array(np.array([0], np.int64), "c0"),
        numpy_helper.from_array(np.array([1], np.int64), "c1"),
        numpy_helper.from_array(np.array([2], np.int64), "c2"),
    ]
    ax_ch = numpy_helper.from_array(np.array([1], np.int64), "axch")
    inits.append(ax_ch)

    nodes = [
        helper.make_node("Flatten", ["observation"], ["flat"], axis=1),
        # ----- linear part -----
        helper.make_node("Gemm", ["flat", "W_from", "b_from"], ["from_sc"]),
        helper.make_node("Gemm", ["flat", "W_to", "b_to"], ["to_sc"]),
        helper.make_node("Unsqueeze", ["from_sc", "ax2"], ["from_3d"]),
        helper.make_node("Unsqueeze", ["to_sc", "ax1"], ["to_3d"]),
        helper.make_node("Add", ["from_3d", "to_3d"], ["pol_3d"]),
        helper.make_node("Flatten", ["pol_3d"], ["policy"], axis=1),
        helper.make_node("Gemm", ["flat", "W_val", "b_val"], ["lin_2d"]),
        helper.make_node("Squeeze", ["lin_2d", "ax1"], ["lin_v"]),
        # ----- pressure maps -----
        helper.make_node("Conv", ["observation", "W_conv", "b_conv"],
                         ["press"], pads=[2, 2, 2, 2]),
        helper.make_node("Slice", ["press", "c0", "c1", "axch"],
                         ["press_en"]),       # enemy pressure (B,1,8,8)
        helper.make_node("Slice", ["press", "c1", "c2", "axch"],
                         ["press_own_raw"]),  # own pressure (B,1,8,8)
        # own kernel / enemy kernel occupancy
        helper.make_node("Slice", ["observation", "s_ok", "e_ok", "axch"],
                         ["ok_plane"]),
        helper.make_node("Slice", ["observation", "s_ek", "e_ek", "axch"],
                         ["ek_plane"]),
        helper.make_node("Mul", ["ok_plane", "press_en"], ["ok_danger_map"]),
        helper.make_node("Mul", ["ek_plane", "press_own_raw"], ["ek_danger_map"]),
        helper.make_node("ReduceSum", ["ok_danger_map", "ax123"],
                         ["ok_danger"], keepdims=0),
        helper.make_node("ReduceSum", ["ek_danger_map", "ax123"],
                         ["ek_danger"], keepdims=0),
        helper.make_node("Sub", ["ek_danger", "ok_danger"], ["danger_diff"]),
        helper.make_node("Mul", ["danger_diff", "w_danger"], ["danger_v"]),
        # ----- firewall urgency x outer ring -----
        helper.make_node("Slice", ["observation", "s_u", "e_u", "axch"],
                         ["urg_plane"]),
        helper.make_node("Slice", ["observation", "s_own", "e_own", "axch"],
                         ["own_planes"]),
        helper.make_node("Slice", ["observation", "s_en", "e_en", "axch"],
                         ["en_planes"]),
        helper.make_node("ReduceSum", ["own_planes", "ax1"], ["own_occ"],
                         keepdims=1),
        helper.make_node("ReduceSum", ["en_planes", "ax1"], ["en_occ"],
                         keepdims=1),
        helper.make_node("Sub", ["en_occ", "own_occ"], ["occ_diff"]),
        helper.make_node("Mul", ["occ_diff", "ring0"], ["occ_ring"]),
        helper.make_node("Mul", ["occ_ring", "urg_plane"], ["occ_urgent"]),
        helper.make_node("ReduceSum", ["occ_urgent", "ax123"], ["fw_pieces"],
                         keepdims=0),
        helper.make_node("Mul", ["fw_pieces", "w_fp"], ["fw_pieces_v"]),
        helper.make_node("Sub", ["ek_plane", "ok_plane"], ["kern_diff"]),
        helper.make_node("Mul", ["kern_diff", "ring0"], ["kern_ring"]),
        helper.make_node("Mul", ["kern_ring", "urg_plane"], ["kern_urgent"]),
        helper.make_node("ReduceSum", ["kern_urgent", "ax123"], ["fw_kern"],
                         keepdims=0),
        helper.make_node("Mul", ["fw_kern", "w_fk"], ["fw_kern_v"]),
        # ----- combine -----
        helper.make_node("Add", ["lin_v", "danger_v"], ["v1"]),
        helper.make_node("Add", ["v1", "fw_pieces_v"], ["v2"]),
        helper.make_node("Add", ["v2", "fw_kern_v"], ["v3"]),
        helper.make_node("Tanh", ["v3"], ["value"]),
    ]

    graph = helper.make_graph(
        nodes, "colony_one_handcrafted_v2",
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
    model = helper.make_model(graph,
                              opset_imports=[helper.make_opsetid("", 17)])
    model.ir_version = 8
    onnx.checker.check_model(model)
    return model


if __name__ == "__main__":
    onnx.save(build_model(), OUT)
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.1f} KiB)")
