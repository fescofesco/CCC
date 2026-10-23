"""Train a small policy/value CNN on self-play data and export ONNX.

Data: selfplay.py npz files (obs, sparse visit-count policy targets, z).
Loss: cross-entropy against the normalized visit distribution + MSE value.
Export: opset 17, dynamic batch, weights embedded, outputs (policy, value).

Usage: python train.py DATA_DIR OUT.onnx [epochs]
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self, ch: int = 64):
        super().__init__()
        self.trunk = nn.Sequential(
            nn.Conv2d(16, ch, 3, padding=1), nn.ReLU(),
            nn.Conv2d(ch, ch, 3, padding=1), nn.ReLU(),
            nn.Conv2d(ch, ch, 3, padding=1), nn.ReLU(),
        )
        self.pol_head = nn.Sequential(
            nn.Conv2d(ch, 2, 1), nn.ReLU(), nn.Flatten(),
            nn.Linear(128, 4096),
        )
        self.val_head = nn.Sequential(
            nn.Conv2d(ch, 2, 1), nn.ReLU(), nn.Flatten(),
            nn.Linear(128, 64), nn.ReLU(), nn.Linear(64, 1), nn.Tanh(),
        )

    def forward(self, x):
        h = self.trunk(x)
        return self.pol_head(h), self.val_head(h).squeeze(-1)


def load(data_dir: Path):
    obs, tgt, z = [], [], []
    for f in sorted(data_dir.glob("worker_*.npz")):
        d = np.load(f)
        o, zi = d["obs"], d["z"]
        off, idx, cnt = d["pol_off"], d["pol_idx"], d["pol_cnt"]
        t = np.zeros((len(o), 4096), np.float32)
        for i in range(len(o)):
            s, e = off[i], off[i + 1]
            c = cnt[s:e]
            t[i, idx[s:e]] = c / max(c.sum(), 1.0)
        obs.append(o); tgt.append(t); z.append(zi)
        print(f"loaded {f.name}: {len(o)} samples")
    return (np.concatenate(obs), np.concatenate(tgt), np.concatenate(z))


def main():
    data_dir, out = Path(sys.argv[1]), Path(sys.argv[2])
    epochs = int(sys.argv[3]) if len(sys.argv) > 3 else 14
    obs, tgt, z = load(data_dir)
    n = len(obs)
    print(f"total {n} samples")
    torch.manual_seed(0)
    model = Net()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    obs_t = torch.from_numpy(obs)
    tgt_t = torch.from_numpy(tgt)
    z_t = torch.from_numpy(z)
    bs = 256
    for ep in range(epochs):
        perm = torch.randperm(n)
        pl_sum = vl_sum = 0.0
        for i in range(0, n - bs + 1, bs):
            b = perm[i:i + bs]
            logits, v = model(obs_t[b])
            pl = -(tgt_t[b] * F.log_softmax(logits, dim=1)).sum(1).mean()
            vl = F.mse_loss(v, z_t[b])
            loss = pl + vl
            opt.zero_grad(); loss.backward(); opt.step()
            pl_sum += float(pl); vl_sum += float(vl)
        nb = max(1, (n - bs + 1) // bs + 1)
        print(f"epoch {ep + 1}: policy {pl_sum / nb:.3f} value {vl_sum / nb:.3f}",
              flush=True)

    model.eval()
    dummy = torch.zeros(1, 16, 8, 8)
    torch.onnx.export(
        model, dummy, out, opset_version=17,
        input_names=["observation"], output_names=["policy", "value"],
        dynamic_axes={"observation": {0: "batch"}, "policy": {0: "batch"},
                      "value": {0: "batch"}},
        dynamo=False,
    )
    print(f"exported {out} ({out.stat().st_size / 1024:.0f} KiB)")


if __name__ == "__main__":
    main()
