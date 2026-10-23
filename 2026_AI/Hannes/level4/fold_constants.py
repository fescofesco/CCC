"""Fold Constant nodes into initializers so the graph passes the allow-list."""
import sys
import onnx
from onnx import numpy_helper

m = onnx.load(sys.argv[1])
g = m.graph
keep = []
for node in g.node:
    if node.op_type == "Constant":
        t = None
        for a in node.attribute:
            if a.name == "value":
                t = a.t
        assert t is not None, "unsupported Constant form"
        t.name = node.output[0]
        g.initializer.append(t)
    else:
        keep.append(node)
del g.node[:]
g.node.extend(keep)
onnx.checker.check_model(m)
onnx.save(m, sys.argv[2])
ops = sorted({n.op_type for n in m.graph.node})
print("ops:", ops)
