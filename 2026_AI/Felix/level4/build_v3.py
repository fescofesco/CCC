"""Parameterized hand-built evaluator for Colony: One (level 4 tuning).

Same graph family as level3/build_model_v2.py plus a policy-safety term:
destination logits are reduced by enemy pressure on the target square, so
the prior avoids hanging pieces; from-logits get a small bonus for moving
pieces that stand under pressure.

Usage: python build_v3.py out.onnx '{"danger":0.5,"pol_safety":0.08,...}'
Any omitted key keeps the default below.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper

N = 8
NUM_SQ = 64
NUM_PLANES = 16
FLAT = NUM_PLANES * NUM_SQ
PING, DAEMON, EXPLOIT, TRACE, ICE, KERNEL = range(6)
ENEMY = 6
URGENCY_PLANE, MAGENTA_PLANE = 14, 15

DEFAULTS = {
    "mat": [15.0, 45.0, 25.0, 30.0, 50.0],          # ping daemon exploit trace ice
    "kernel_ring": [0.0, 4.0, 9.0, 12.0],
    "piece_ring": 0.3,
    "scale": 1.0 / 120.0,
    "threat": [6.0, 10.0, 8.0, 7.0, 10.0, 4.0],     # per piece type
    "danger": 1.0,
    "danger_ek_mult": 1.0,   # mover weighs its threat on enemy kernel higher
    "fw_kernel": 25.0,
    "fw_piece": 6.0,
    "capture": [2.0, 3.6, 2.5, 3.0, 4.0, 8.0],
    "to_center": 0.25,
    "from_piece": [0.4, 0.4, 0.5, 0.4, 0.4, 0.0],
    "pol_safety": 0.0,       # to-logit -= this * enemy pressure at target
    "pol_escape": 0.0,       # from-logit += this * enemy pressure at origin
    "kernel_ring_late": [0.0, 0.0, 0.0, 0.0],  # extra, scaled by locked frac
}


def ring(sq: int) -> int:
    r, c = divmod(sq, N)
    return min(r, N - 1 - r, c, N - 1 - c)


def build(params: dict, out: Path) -> None:
    p = {**DEFAULTS, **params}
    mat = {i: v for i, v in enumerate(p["mat"])}
    scale = p["scale"]

    w_val = np.zeros(FLAT, dtype=np.float32)
    for sq in range(NUM_SQ):
        rg = ring(sq)
        for pi, m in mat.items():
            w_val[pi * NUM_SQ + sq] = m + p["piece_ring"] * rg
            w_val[(ENEMY + pi) * NUM_SQ + sq] = -(m + p["piece_ring"] * rg)
        w_val[KERNEL * NUM_SQ + sq] = p["kernel_ring"][rg]
        w_val[(ENEMY + KERNEL) * NUM_SQ + sq] = -p["kernel_ring"][rg]
        w_val[MAGENTA_PLANE * NUM_SQ + sq] = 2.0 / NUM_SQ
    w_val *= scale

    w_to = np.zeros((FLAT, NUM_SQ), dtype=np.float32)
    b_to = np.array([p["to_center"] * ring(j) for j in range(NUM_SQ)],
                    dtype=np.float32)
    w_from = np.zeros((FLAT, NUM_SQ), dtype=np.float32)
    for sq in range(NUM_SQ):
        for pi in range(6):
            w_to[(ENEMY + pi) * NUM_SQ + sq, sq] = p["capture"][pi]
            w_from[pi * NUM_SQ + sq, sq] = p["from_piece"][pi]

    # 7x7 pressure window: sliders (Ice, Daemon, Trace) strike at range 2-3
    kern7 = np.zeros((7, 7), dtype=np.float32)
    for dr in range(-3, 4):
        for dc in range(-3, 4):
            d = max(abs(dr), abs(dc))
            kern7[dr + 3, dc + 3] = {0: 3.0, 1: 2.5, 2: 1.5, 3: 0.75}[d]
    kern_def = kern7.copy()
    kern_def[3, 3] = 0.0  # defense map: pressure from OTHER squares only
    w_conv = np.zeros((3, NUM_PLANES, 7, 7), dtype=np.float32)
    for pi in range(6):
        w_conv[0, ENEMY + pi] = kern7 * p["threat"][pi]
        w_conv[1, pi] = kern7 * p["threat"][pi]
        w_conv[2, ENEMY + pi] = kern_def * p["threat"][pi]

    ring0 = np.zeros((1, 1, N, N), dtype=np.float32)
    kr_late = np.zeros((1, 1, N, N), dtype=np.float32)
    for sq in range(NUM_SQ):
        if ring(sq) == 0:
            ring0[0, 0, sq // N, sq % N] = 1.0
        kr_late[0, 0, sq // N, sq % N] = p["kernel_ring_late"][ring(sq)]

    i64 = lambda name, vals: numpy_helper.from_array(
        np.array(vals, np.int64), name)
    f32 = lambda name, arr: numpy_helper.from_array(
        np.asarray(arr, np.float32), name)

    inits = [
        f32("W_from", w_from), f32("b_from", np.zeros(NUM_SQ)),
        f32("W_to", w_to), f32("b_to", b_to),
        f32("W_val", w_val.reshape(FLAT, 1)), f32("b_val", np.zeros(1)),
        f32("W_conv", w_conv), f32("b_conv", np.zeros(3)),
        f32("ring0", ring0),
        f32("w_danger", np.array(p["danger"] * scale)),
        f32("w_fk", np.array(p["fw_kernel"] * scale)),
        f32("w_fp", np.array(p["fw_piece"] * scale)),
        f32("w_psafe", np.array(p["pol_safety"])),
        f32("w_pesc", np.array(p["pol_escape"])),
        i64("ax1", [1]), i64("ax2", [2]), i64("ax123", [1, 2, 3]),
        i64("axch", [1]), i64("c0", [0]), i64("c1", [1]), i64("c2", [2]),
        i64("c3", [3]),
        i64("s_ok", [KERNEL]), i64("e_ok", [KERNEL + 1]),
        i64("s_ek", [ENEMY + KERNEL]), i64("e_ek", [ENEMY + KERNEL + 1]),
        i64("s_own", [0]), i64("e_own", [ENEMY]),
        i64("s_en", [ENEMY]), i64("e_en", [2 * ENEMY]),
        i64("s_u", [URGENCY_PLANE]), i64("e_u", [URGENCY_PLANE + 1]),
        i64("s_l", [12]), i64("e_l", [13]),
        f32("one", np.array(1.0)),
        f32("kr_late", kr_late),
        f32("inv28", np.array(scale / 28.0)),
        f32("w_ekmult", np.array(p["danger_ek_mult"])),
    ]

    nodes = [
        helper.make_node("Flatten", ["observation"], ["flat"], axis=1),
        helper.make_node("Gemm", ["flat", "W_from", "b_from"], ["from_lin"]),
        helper.make_node("Gemm", ["flat", "W_to", "b_to"], ["to_lin"]),
        helper.make_node("Conv", ["observation", "W_conv", "b_conv"],
                         ["press"], pads=[3, 3, 3, 3]),
        helper.make_node("Slice", ["press", "c0", "c1", "axch"], ["press_en"]),
        helper.make_node("Slice", ["press", "c1", "c2", "axch"], ["press_own"]),
        helper.make_node("Slice", ["press", "c2", "c3", "axch"], ["press_def"]),
        # policy safety: to -= w_psafe*defended ; from += w_pesc*defended
        helper.make_node("Flatten", ["press_def"], ["press_def_flat"], axis=1),
        helper.make_node("Mul", ["press_def_flat", "w_psafe"], ["to_pen"]),
        helper.make_node("Sub", ["to_lin", "to_pen"], ["to_sc"]),
        helper.make_node("Mul", ["press_def_flat", "w_pesc"], ["from_bon"]),
        helper.make_node("Add", ["from_lin", "from_bon"], ["from_sc"]),
        helper.make_node("Unsqueeze", ["from_sc", "ax2"], ["from_3d"]),
        helper.make_node("Unsqueeze", ["to_sc", "ax1"], ["to_3d"]),
        helper.make_node("Add", ["from_3d", "to_3d"], ["pol_3d"]),
        helper.make_node("Flatten", ["pol_3d"], ["policy"], axis=1),
        # value
        helper.make_node("Gemm", ["flat", "W_val", "b_val"], ["lin_2d"]),
        helper.make_node("Squeeze", ["lin_2d", "ax1"], ["lin_v"]),
        helper.make_node("Slice", ["observation", "s_ok", "e_ok", "axch"],
                         ["ok_plane"]),
        helper.make_node("Slice", ["observation", "s_ek", "e_ek", "axch"],
                         ["ek_plane"]),
        helper.make_node("Mul", ["ok_plane", "press_en"], ["okd_map"]),
        helper.make_node("Mul", ["ek_plane", "press_own"], ["ekd_map"]),
        helper.make_node("ReduceSum", ["okd_map", "ax123"], ["okd"], keepdims=0),
        helper.make_node("ReduceSum", ["ekd_map", "ax123"], ["ekd"], keepdims=0),
        helper.make_node("Mul", ["ekd", "w_ekmult"], ["ekd_m"]),
        helper.make_node("Sub", ["ekd_m", "okd"], ["dd"]),
        helper.make_node("Mul", ["dd", "w_danger"], ["danger_v"]),
        helper.make_node("Slice", ["observation", "s_u", "e_u", "axch"],
                         ["urg"]),
        helper.make_node("Slice", ["observation", "s_own", "e_own", "axch"],
                         ["own_pl"]),
        helper.make_node("Slice", ["observation", "s_en", "e_en", "axch"],
                         ["en_pl"]),
        helper.make_node("ReduceSum", ["own_pl", "ax1"], ["own_occ"],
                         keepdims=1),
        helper.make_node("ReduceSum", ["en_pl", "ax1"], ["en_occ"],
                         keepdims=1),
        # burning ring = not-locked squares adjacent (8-way) to locked or
        # off-board; works at every shrink stage.
        helper.make_node("Slice", ["observation", "s_l", "e_l", "axch"],
                         ["locked"]),
        helper.make_node("MaxPool", ["locked"], ["nbl"],
                         kernel_shape=[3, 3], pads=[1, 1, 1, 1],
                         strides=[1, 1]),
        helper.make_node("Max", ["nbl", "ring0"], ["nbl2"]),
        helper.make_node("Sub", ["one", "locked"], ["notlocked"]),
        helper.make_node("Mul", ["nbl2", "notlocked"], ["burn"]),
        helper.make_node("Sub", ["en_occ", "own_occ"], ["occ_d"]),
        helper.make_node("Mul", ["occ_d", "burn"], ["occ_r"]),
        helper.make_node("Mul", ["occ_r", "urg"], ["occ_u"]),
        helper.make_node("ReduceSum", ["occ_u", "ax123"], ["fwp"], keepdims=0),
        helper.make_node("Mul", ["fwp", "w_fp"], ["fwp_v"]),
        helper.make_node("Sub", ["ek_plane", "ok_plane"], ["kd"]),
        helper.make_node("Mul", ["kd", "burn"], ["kd_r"]),
        helper.make_node("Mul", ["kd_r", "urg"], ["kd_u"]),
        helper.make_node("ReduceSum", ["kd_u", "ax123"], ["fwk"], keepdims=0),
        helper.make_node("Mul", ["fwk", "w_fk"], ["fwk_v"]),
        # late-game kernel centrality: extra ring bonus x locked fraction
        helper.make_node("Sub", ["ok_plane", "ek_plane"], ["kdiff2"]),
        helper.make_node("Mul", ["kdiff2", "kr_late"], ["klate_map"]),
        helper.make_node("ReduceSum", ["klate_map", "ax123"], ["klate"],
                         keepdims=0),
        helper.make_node("ReduceSum", ["locked", "ax123"], ["lockedsum"],
                         keepdims=0),
        helper.make_node("Mul", ["klate", "lockedsum"], ["klate_s"]),
        helper.make_node("Mul", ["klate_s", "inv28"], ["klate_v"]),
        helper.make_node("Add", ["lin_v", "danger_v"], ["v1"]),
        helper.make_node("Add", ["v1", "fwp_v"], ["v2"]),
        helper.make_node("Add", ["v2", "fwk_v"], ["v3"]),
        helper.make_node("Add", ["v3", "klate_v"], ["v4"]),
        helper.make_node("Tanh", ["v4"], ["value"]),
    ]

    graph = helper.make_graph(
        nodes, "colony_one_v3",
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
    onnx.save(model, out)
    print(f"wrote {out} ({out.stat().st_size / 1024:.1f} KiB)")


if __name__ == "__main__":
    out = Path(sys.argv[1])
    params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    build(params, out)
