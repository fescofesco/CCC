"""Aggregate all match dumps in ./matches (json + txt), dedupe, report."""
import json, re, sys
from pathlib import Path
M = Path(__file__).resolve().parent / "matches"
games = {}
for f in M.glob("tournament-matches*.json"):
    for m in json.load(open(f)):
        p = m.get("protocol")
        if p: games[m["match_id"]] = (m.get("you"), p, m.get("played_at", ""))
for f in M.glob("match-*.txt"):
    mid = int(re.search(r"(\d+)", f.name).group(1))
    if mid not in games:
        games[mid] = (None, f.read_text(), "")
rows = []
for mid, (you, p, at) in sorted(games.items()):
    winner = "CYAN" if "CYAN WINS" in p else "MAGENTA"
    term = "capture"
    if re.search(r"FIREWALL ROUND \d+: \[[^\]]*KE", p): term = "firewall-KE"
    if "BARE KERNEL" in p: term = "bare-kernel"
    nact = len(re.findall(r"^\s*\d+\.", p, re.M))
    res = "?" if you is None else ("W" if winner == you else "L")
    rows.append((mid, at[11:19] if at else "?", you or "?", res, term, nact))
w = sum(1 for r in rows if r[3] == "W"); l = sum(1 for r in rows if r[3] == "L")
print(f"{len(rows)} matches known: {w}W {l}L ({len(rows)-w-l} side-unknown)")
print("last 12:")
for r in rows[-12:]: print(" ", *r)
print("losses by termination:")
from collections import Counter
print(" ", Counter(r[4] for r in rows if r[3] == "L"))
