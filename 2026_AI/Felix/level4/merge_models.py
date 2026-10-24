"""Splice two Colony: One ONNX evaluators into one blended model.

Both inputs must have the contract (observation -> policy, value). The
merged graph feeds one shared observation into both subgraphs and blends:
  policy = wa_p * policy_A + wb_p * policy_B
  value  = wa_v * value_A  + wb_v * value_B   (wa_v + wb_v = 1 keeps [-1,1])

Usage: python merge_models.py A.onnx B.onnx OUT.onnx wa_p wb_p wa_v wb_v
"""
from __future__ import annotations

import sys

import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper
from onnx.compose import add_prefix


def main() -> None:
    path_a, path_b, out = sys.argv[1], sys.argv[2], sys.argv[3]
    wa_p, wb_p, wa_v, wb_v = (float(x) for x in sys.argv[4:8])

    a = add_prefix(onnx.load(path_a), "a_")
    b = add_prefix(onnx.load(path_b), "b_")

    nodes = [
        helper.make_node("Identity", ["observation"], ["a_observation"]),
        helper.make_node("Identity", ["observation"], ["b_observation"]),
    ]
    nodes += list(a.graph.node) + list(b.graph.node)

    f32 = lambda name, v: numpy_helper.from_array(np.array(v, np.float32), name)
    inits = list(a.graph.initializer) + list(b.graph.initializer) + [
        f32("m_wap", wa_p), f32("m_wbp", wb_p),
        f32("m_wav", wa_v), f32("m_wbv", wb_v),
    ]
    nodes += [
        helper.make_node("Mul", ["a_policy", "m_wap"], ["m_pa"]),
        helper.make_node("Mul", ["b_policy", "m_wbp"], ["m_pb"]),
        helper.make_node("Add", ["m_pa", "m_pb"], ["policy"]),
        helper.make_node("Mul", ["a_value", "m_wav"], ["m_va"]),
        helper.make_node("Mul", ["b_value", "m_wbv"], ["m_vb"]),
        helper.make_node("Add", ["m_va", "m_vb"], ["value"]),
    ]

    graph = helper.make_graph(
        nodes, "kernel76_fusion",
        inputs=[helper.make_tensor_value_info(
            "observation", TensorProto.FLOAT, ["batch", 16, 8, 8])],
        outputs=[
            helper.make_tensor_value_info(
                "policy", TensorProto.FLOAT, ["batch", 4096]),
            helper.make_tensor_value_info(
                "value", TensorProto.FLOAT, ["batch"]),
        ],
        initializer=inits,
    )
    opset = max(
        [o.version for o in list(a.opset_import) + list(b.opset_import)
         if o.domain in ("", "ai.onnx")] + [17])
    model = helper.make_model(
        graph, opset_imports=[helper.make_opsetid("", opset)])
    model.ir_version = 8
    model.producer_name = "fehalu"
    onnx.checker.check_model(model)
    onnx.save(model, out)
    print(f"wrote {out} (opset {opset})")


if __name__ == "__main__":
    main()
