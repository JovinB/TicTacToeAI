from typing import NamedTuple
from itertools import cycle


class Player(NamedTuple):
    label: str
    colour: str


class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


DEFAULT_PLAYERS = (
    Player(label="X", colour="blue"),
    Player(label="O", colour="red"),
)


class Game:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=3):
        self.players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self.players)
        self.winner_combo = []
        self.current_moves = []
        self.has_winner = False
        self.winning_combos = []
        self.setup_board()

    def setup_board(self):
        self.current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self.winning_combos = self.get_winning_combos()
