"""
colony.py - rules engine for the Cloudflight Coding Contest "Colony: One".

Classes only, no workflow: a main script imports these and runs them.

Board text format (top row first, 8 rows x 8 tiles, whitespace ignored):
    K  P   CYAN Kernel / Ping   (you)
    k  p   MAGENTA Kernel / Ping
    .      empty tile
Tiles are named chess-style: columns a-h left to right, rows 8-1 top to bottom.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

SIZE = 8
CYAN, MAGENTA = "CYAN", "MAGENTA"
KERNEL, PING = "K", "P"
ACTIONS_PER_TURN = 2

Pos = tuple[int, int]  # (row, col), row 0 = top

# "any adjacent tile" = the 8 neighbours. Remove the diagonals here if the game uses only 4.
KERNEL_STEPS = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if (dr, dc) != (0, 0)]
ORTHOGONAL = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIAGONAL = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
ARROW = {(-1, 0): "↑", (1, 0): "↓", (0, -1): "←", (0, 1): "→",
         (-1, -1): "↖", (-1, 1): "↗", (1, -1): "↙", (1, 1): "↘"}


def other(team: str) -> str:
    return MAGENTA if team == CYAN else CYAN


def on_board(pos: Pos) -> bool:
    return 0 <= pos[0] < SIZE and 0 <= pos[1] < SIZE


def tile_name(pos: Pos) -> str:
    return "abcdefgh"[pos[1]] + str(SIZE - pos[0])


@dataclass(frozen=True)
class Piece:
    team: str
    kind: str  # KERNEL or PING

    @property
    def symbol(self) -> str:
        return self.kind if self.team == CYAN else self.kind.lower()


@dataclass(frozen=True)
class Action:
    piece: Piece
    start: Pos
    end: Pos
    captured: Piece | None = None

    @property
    def takes_kernel(self) -> bool:
        return self.captured is not None and self.captured.kind == KERNEL

    def __str__(self) -> str:
        dr, dc = self.end[0] - self.start[0], self.end[1] - self.start[1]
        n = max(abs(dr), abs(dc))
        text = f"{self.piece.symbol} {tile_name(self.start)}→{tile_name(self.end)} {ARROW[(dr // n, dc // n)] * n}"
        return text + (f" (takes {self.captured.symbol})" if self.captured else "")


class Board:
    """A position: {(row, col): Piece}. Never mutated; apply() returns a new Board."""

    SYMBOLS = {"K": Piece(CYAN, KERNEL), "P": Piece(CYAN, PING),
               "k": Piece(MAGENTA, KERNEL), "p": Piece(MAGENTA, PING)}

    def __init__(self, pieces: dict[Pos, Piece]):
        self.pieces = pieces

    @classmethod
    def from_text(cls, text: str) -> Board:
        rows = ["".join(line.split()) for line in text.strip().splitlines() if line.strip()]
        if len(rows) != SIZE or any(len(row) != SIZE for row in rows):
            raise ValueError(f"expected {SIZE} rows of {SIZE} tiles, got row lengths {[len(r) for r in rows]}")
        pieces = {}
        for r, row in enumerate(rows):
            for c, ch in enumerate(row):
                if ch in cls.SYMBOLS:
                    pieces[(r, c)] = cls.SYMBOLS[ch]
                elif ch != ".":
                    raise ValueError(f"unknown symbol {ch!r} on {tile_name((r, c))}")
        return cls(pieces)

    def kernel(self, team: str) -> Pos | None:
        return next((pos for pos, p in self.pieces.items() if p.team == team and p.kind == KERNEL), None)

    # ---- move generation -------------------------------------------------
    def actions(self, team: str) -> Iterator[Action]:
        for pos, piece in self.pieces.items():
            if piece.team == team:
                generate = self._kernel_actions if piece.kind == KERNEL else self._ping_actions
                yield from generate(pos, piece)

    def _kernel_actions(self, pos: Pos, piece: Piece) -> Iterator[Action]:
        for dr, dc in KERNEL_STEPS:                      # 1 step, captures whatever enemy stands there
            end = (pos[0] + dr, pos[1] + dc)
            target = self.pieces.get(end)
            if on_board(end) and (target is None or target.team != piece.team):
                yield Action(piece, pos, end, target)

    def _ping_actions(self, pos: Pos, piece: Piece) -> Iterator[Action]:
        for dr, dc in ORTHOGONAL:                        # move 1-2 tiles onto empty tiles, no jumping
            for dist in (1, 2):
                end = (pos[0] + dr * dist, pos[1] + dc * dist)
                if not on_board(end) or end in self.pieces:
                    break
                yield Action(piece, pos, end)
        for dr, dc in DIAGONAL:                          # capture the first piece within 2 diagonal tiles
            for dist in (1, 2):
                end = (pos[0] + dr * dist, pos[1] + dc * dist)
                if not on_board(end):
                    break
                target = self.pieces.get(end)
                if target is not None:
                    if target.team != piece.team:
                        yield Action(piece, pos, end, target)
                    break

    def apply(self, action: Action) -> Board:
        pieces = dict(self.pieces)
        del pieces[action.start]
        pieces[action.end] = action.piece
        return Board(pieces)

    # ---- lookahead ---------------------------------------------------------
    def can_take_kernel(self, attacker: str, actions: int = ACTIONS_PER_TURN) -> bool:
        """True if `attacker` can capture the other team's Kernel within `actions` actions."""
        if actions == 0:
            return False
        return any(a.takes_kernel or self.apply(a).can_take_kernel(attacker, actions - 1)
                   for a in self.actions(attacker))

    def render(self, marks: dict[Pos, str] | None = None) -> str:
        marks = marks or {}
        lines = ["    " + " ".join("abcdefgh"[:SIZE])]
        for r in range(SIZE):
            cells = [marks.get((r, c)) or (self.pieces[(r, c)].symbol if (r, c) in self.pieces else ".")
                     for c in range(SIZE)]
            lines.append(f" {SIZE - r}  " + " ".join(cells))
        return "\n".join(lines)


@dataclass
class Plan:
    """One complete turn for our team and what MAGENTA can do about it."""
    actions: tuple[Action, ...]
    result: Board
    wins: bool
    danger: int | None  # MAGENTA actions needed to take our Kernel afterwards (None = safe)

    @property
    def safe(self) -> bool:
        return self.danger is None

    @property
    def captures(self) -> int:
        return sum(a.captured is not None for a in self.actions)

    @property
    def kernel_only(self) -> bool:
        return all(a.piece.kind == KERNEL for a in self.actions)

    def __str__(self) -> str:
        return ",  ".join(str(a) for a in self.actions)


class TurnSolver:
    """Level 1: every two-action turn after which the enemy cannot take our Kernel in its turn."""

    MAX_LISTED = 10

    def __init__(self, board: Board, team: str = CYAN):
        if board.kernel(team) is None:
            raise ValueError(f"{team} has no Kernel on the board")
        self.board, self.team, self.enemy = board, team, other(team)

    def _danger(self, board: Board) -> int | None:
        for n in range(1, ACTIONS_PER_TURN + 1):
            if board.can_take_kernel(self.enemy, n):
                return n
        return None

    def plans(self) -> list[Plan]:
        plans = []
        for first in self.board.actions(self.team):
            after_first = self.board.apply(first)
            if first.takes_kernel:                       # game over on the spot
                plans.append(Plan((first,), after_first, True, None))
                continue
            for second in after_first.actions(self.team):
                result = after_first.apply(second)
                wins = second.takes_kernel
                plans.append(Plan((first, second), result, wins, None if wins else self._danger(result)))
        return plans

    def report(self) -> str:
        plans = self.plans()
        start = self.board.kernel(self.team)

        marks = {}                                       # where can the Kernel end up, and is it safe there?
        for p in plans:
            end = p.result.kernel(self.team)
            if p.kernel_only and end != start:
                marks[end] = "S" if p.safe or marks.get(end) == "S" else "x"
        lines = [f"{left}      {right}" for left, right in
                 zip(self.board.render().splitlines(), self.board.render(marks).splitlines())]
        lines += ["    scene as typed             S = safe end tile, x = MAGENTA can take you there", ""]

        winners = [p for p in plans if p.wins]
        if winners:
            return "\n".join(lines + ["WIN, take MAGENTA's Kernel:", f"  {winners[0]}"])

        safe = [p for p in plans if p.safe]
        candidates = safe or [p for p in plans if p.danger == 2]
        best = {}                                        # one line per distinct resulting position
        for p in sorted(candidates, key=lambda p: (-p.captures, not p.kernel_only,
                                                   tile_name(p.result.kernel(self.team)))):
            best.setdefault(frozenset(p.result.pieces.items()), p)
        if safe:
            lines.append(f"{len(best)} safe turn(s):")
        elif best:
            lines.append("No fully safe turn. These at least survive MAGENTA's first action:")
        else:
            lines.append("No turn survives: MAGENTA can take your Kernel whatever you play.")
        shown = list(best.values())
        lines += [f"  {i}. {p}" for i, p in enumerate(shown[:self.MAX_LISTED], 1)]
        if len(shown) > self.MAX_LISTED:
            lines.append(f"  ... and {len(shown) - self.MAX_LISTED} more")
        return "\n".join(lines)
