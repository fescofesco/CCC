"""
colony2.py - Colony: One rules up to Level 2 (bodyguard, firewall, kernel endgame)
and a forced-win search for CYAN. Tools only; play_level2.py drives it.

Position syntax: one token per piece, uppercase = CYAN, lowercase = MAGENTA,
K = Kernel, P = Ping, e.g.  "kb5 Pe2 Kh2".
"""
CY, MG = 0, 1
KER, PIN = "K", "P"
FIREWALL = {8: 1, 16: 2, 24: 3, 26: 4}      # end of round -> outer rings gone
LAST_ROUND = 26
FILES = "abcdefgh"

def name(p): r, c = divmod(p, 8); return FILES[c] + str(8 - r)
def tile(s):
    s = s.strip().lower()
    if len(s) != 2 or s[0] not in FILES or s[1] not in "12345678": raise ValueError(f"bad tile {s!r}")
    return (8 - int(s[1])) * 8 + FILES.index(s[0])
RING = [min(p // 8, p % 8, 7 - p // 8, 7 - p % 8) for p in range(64)]
def step(p, dr, dc, n=1):
    r, c = divmod(p, 8); r += dr * n; c += dc * n
    return r * 8 + c if 0 <= r < 8 and 0 <= c < 8 else -1
KSTEPS = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)]
ORTH = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIAG = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
NEIGH = [[q for d in KSTEPS if (q := step(p, *d)) >= 0] for p in range(64)]
def cheb(a, b): return max(abs(a // 8 - b // 8), abs(a % 8 - b % 8))
def other(t): return 1 - t
def on(p, mr): return p >= 0 and RING[p] >= mr
def key(board): return tuple(sorted(board.items()))


def parse(spec):
    board = {}
    for tok in spec.replace(",", " ").split():
        if tok[0].upper() not in "KP": raise ValueError(f"bad piece {tok!r}")
        board[tile(tok[1:])] = (CY if tok[0].isupper() else MG, tok[0].upper())
    return board


class Game:
    """Rules: action generation, a full 2-action turn, and end-of-turn effects."""

    @staticmethod
    def _attack(board, t, p, q, kind):
        tq, kq = board[q]
        if kq == KER:
            guards = [g for g in NEIGH[q] if g in board and board[g][0] == tq]
            if guards:                               # bodyguard dies, attacker stays put
                for g in guards:
                    nb = dict(board); del nb[g]
                    yield (kind, p, q, f"hits guard on {name(g)}"), nb, None
                return
            nb = dict(board); del nb[p]; nb[q] = (t, kind)
            yield (kind, p, q, "takes the KERNEL"), nb, t
        else:
            nb = dict(board); del nb[p]; nb[q] = (t, kind)
            yield (kind, p, q, f"takes {kq}"), nb, None

    @classmethod
    def actions(cls, board, t, mr):
        for p, (team, kind) in list(board.items()):
            if team != t:
                continue
            if kind == KER:
                for q in NEIGH[p]:
                    if not on(q, mr): continue
                    occ = board.get(q)
                    if occ is None:
                        nb = dict(board); del nb[p]; nb[q] = (t, KER)
                        yield (KER, p, q, ""), nb, None
                    elif occ[0] != t:
                        yield from cls._attack(board, t, p, q, KER)
            else:
                for d in ORTH:
                    for n in (1, 2):
                        q = step(p, *d, n)
                        if not on(q, mr) or q in board: break
                        nb = dict(board); del nb[p]; nb[q] = (t, PIN)
                        yield (PIN, p, q, ""), nb, None
                for d in DIAG:
                    for n in (1, 2):
                        q = step(p, *d, n)
                        if not on(q, mr): break
                        occ = board.get(q)
                        if occ is None: continue
                        if occ[0] != t:
                            yield from cls._attack(board, t, p, q, PIN)
                        break

    @classmethod
    def turns(cls, board, t, mr):
        """Distinct outcomes of a 2-action turn: [(actions, board, winner_or_None)]."""
        seen, out = set(), []
        for a1, b1, w1 in cls.actions(board, t, mr):
            if w1 is not None:
                out.append(((a1,), b1, w1)); continue
            any2 = False
            for a2, b2, w2 in cls.actions(b1, t, mr):
                any2 = True
                k = (key(b2), w2)
                if k not in seen:
                    seen.add(k); out.append(((a1, a2), b2, w2))
            if not any2:
                out.append(((a1,), b1, None))
        return out

    @staticmethod
    def endgame(board, finished):
        if len(board) != 2 or any(v[1] != KER for v in board.values()): return None
        cy = next(p for p, v in board.items() if v[0] == CY)
        mg = next(p for p, v in board.items() if v[0] == MG)
        if cheb(cy, mg) <= 2: return other(finished)
        return CY if RING[cy] > RING[mg] else MG

    @classmethod
    def end_of_turn(cls, board, t, mr, rnd):
        """-> (winner_or_None, board, min_ring, round) for whoever moves next."""
        w = cls.endgame(board, t)
        if w is not None: return w, board, mr, rnd
        if t == MG:
            if rnd in FIREWALL:
                nmr = FIREWALL[rnd]
                dead_k = {board[p][0] for p in board if RING[p] < nmr and board[p][1] == KER}
                if dead_k: return (MG if MG in dead_k else CY), board, mr, rnd
                board = {p: v for p, v in board.items() if RING[p] >= nmr}; mr = nmr
                if cls.endgame(board, MG) == MG: return MG, board, mr, rnd   # cautious reading
            if rnd >= LAST_ROUND: return MG, board, mr, rnd
            rnd += 1
        return None, board, mr, rnd


class Solver:
    """AND-OR search: a CYAN turn that wins against every MAGENTA reply within n CYAN turns."""

    def __init__(self):
        self.memo_c, self.memo_m = {}, {}

    @staticmethod
    def _spread(board):
        m = next((p for p, v in board.items() if v == (MG, KER)), None)
        return 0 if m is None else sum(cheb(m, p) for p, v in board.items() if v[0] == CY)

    def cyan(self, board, mr, rnd, n):
        k = (key(board), mr, rnd, n)
        if k in self.memo_c: return self.memo_c[k]
        res, nxt = None, []
        for acts, b, w in Game.turns(board, CY, mr):
            if w == CY: res = acts; break
            if w == MG: continue
            w2, b2, mr2, rnd2 = Game.end_of_turn(b, CY, mr, rnd)
            if w2 == CY: res = acts; break
            if w2 is None: nxt.append((acts, b2, mr2, rnd2))
        if res is None:
            nxt.sort(key=lambda x: self._spread(x[1]))
            res = next((a for a, b2, mr2, rnd2 in nxt if self.magenta_lost(b2, mr2, rnd2, n)), None)
        self.memo_c[k] = res
        return res

    def magenta_lost(self, board, mr, rnd, n):
        k = (key(board), mr, rnd, n)
        if k in self.memo_m: return self.memo_m[k]
        pending, lost = [], True
        for acts, b, w in Game.turns(board, MG, mr):
            if w == CY: continue
            if w == MG: lost = False; break
            w2, b2, mr2, rnd2 = Game.end_of_turn(b, MG, mr, rnd)
            if w2 == CY: continue
            if w2 == MG or n == 1: lost = False; break
            pending.append((b2, mr2, rnd2))
        if lost:
            pending.sort(key=lambda x: -self._spread(x[0]))
            lost = all(self.cyan(b2, mr2, rnd2, n - 1) is not None for b2, mr2, rnd2 in pending)
        self.memo_m[k] = lost
        return lost

    def best_turn(self, board, mr, rnd, max_turns=10):
        for n in range(1, max_turns + 1):
            acts = self.cyan(board, mr, rnd, n)
            if acts: return acts, n
        return None, None


ARROW = {(-1, 0): "↑", (1, 0): "↓", (0, -1): "←", (0, 1): "→",
         (-1, -1): "↖", (-1, 1): "↗", (1, -1): "↙", (1, 1): "↘"}

def describe(acts):
    out = []
    for kind, p, q, note in acts:
        dr, dc = q // 8 - p // 8, q % 8 - p % 8
        n = max(abs(dr), abs(dc))
        s = f"{kind} {name(p)}→{name(q)} {ARROW[(dr // n, dc // n)] * n}"
        out.append(s + (f" ({note})" if note else ""))
    return ",  then ".join(out)

def render(board, mr=0):
    rows = ["    a b c d e f g h"]
    for r in range(8):
        cells = []
        for c in range(8):
            p = r * 8 + c
            v = board.get(p)
            cells.append(" " if RING[p] < mr else "." if v is None else (v[1] if v[0] == CY else v[1].lower()))
        rows.append(f" {8 - r}  " + " ".join(cells))
    return "\n".join(rows)
