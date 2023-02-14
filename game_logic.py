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
    def __init__(self, players=DEFAULT_PLAYERS):
        self.players = cycle(players)
        self.board_size = 3
        self.current_player = next(self.players)
        self.winner_combo = []
        self.current_moves = []
        self.has_winner = False
        self.winner = ""
        self.winning_combos = []
        self.setup_board()

    def setup_board(self):
        self.current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self.winning_combos = self.get_winning_combos()

    def get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self.current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def is_move_valid(self, move):
        row, col = move.row, move.col
        move_was_not_played = self.current_moves[row][col].label == ""
        no_winner = not self.has_winner
        return no_winner and move_was_not_played

    def isWinner(self, board, current_player):
        for combo in self.winning_combos:
            won = True
            for r, c in combo:
                if board[r][c].label != current_player:
                    won = False

            if won:
                return True, combo
        return False, None

    def perform_action(self, move):
        row, col, label = move.row, move.col, move.label
        self.current_moves[row][col] = move

        return_val = self.isWinner(self.current_moves, self.current_player.label)

        if return_val[0]:
            self.has_winner = True
            self.winner = self.current_player.label
            self.winner_combo = return_val[1]

    def ai_move(self):
        bestScore = -1
        bestMove = ()
        for row in range(3):
            for col in range(3):
                if self.current_moves[row][col].label == "":

                    self.current_moves[row][col] = Move(row,col,self.current_player.label)
                    score = self.findBestMove(self.current_moves, 0, False)
                    self.current_moves[row][col] = Move(row,col,"")

                    if score > bestScore:
                        bestScore = score
                        bestMove = (row,col)

        move = Move(bestMove[0], bestMove[1], self.current_player.label)
        self.current_moves[bestMove[0]][bestMove[1]] = move

        returnVal = self.isWinner(self.current_moves, self.current_player.label)

        if returnVal[0]:
            self.has_winner = True
            self.winner = self.current_player.label
            self.winner_combo = returnVal[1]

        return move

    def findBestMove(self, board, depth, isMax):
        if isMax:
            returnVal = self.isWinner(board, "X")
        else:
            returnVal = self.isWinner(board, "O")

        # if it's max turn, then if there is a winner, the winner is min, as max has not made their move yet
        if returnVal[0]:
            if isMax:
                return -1
            else:
                return 1
        elif self.is_tied():
            return 0

        # ai's turn (max turn)
        if isMax:
            maxScore = -1
            for row in range(3):
                for col in range(3):
                    if board[row][col].label == "":
                        board[row][col] = Move(row, col, "O")
                        score = self.findBestMove(self.current_moves, depth+1, False)
                        board[row][col] = Move(row, col, "")

                        maxScore = max(score, maxScore)

            return maxScore

        # player's turn (min turn)
        else:
            minScore = 1
            for row in range(3):
                for col in range(3):
                    if board[row][col].label == "":
                        board[row][col] = Move(row, col, "X")
                        score = self.findBestMove(self.current_moves, depth+1, True)
                        board[row][col] = Move(row, col, "")

                        minScore = min(score, minScore)

            return minScore

    def is_tied(self):
        no_winner = not self.has_winner
        played_moves = (
            move.label for row in self.current_moves for move in row
        )
        return no_winner and all(played_moves)

    def next_player(self):
        self.current_player = next(self.players)

    def reset_game(self):
        for row, row_content in enumerate(self.current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self.has_winner = False
        self.winner_combo = []
