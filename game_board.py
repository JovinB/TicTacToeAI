import tkinter as tk
from tkinter import font

from game_logic import *

class Board(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.display = None
        self.title("TicTacToe")
        self.tiles = {}
        self.create_main_window()
        self.create_board()

    def create_main_window(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def create_board(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(3):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(3):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self.tiles[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

    def play(self, event):
        button = event.widget
        row, col = self.tiles[button]
        move = Move(row, col, self.game.current_player.label)
        if self.game.is_move_valid(move):
            self.update_button(button)
            self.game.perform_action(move)
            if self.game.is_tied():
                self.update_display(msg="Tied game!", color="red")
            elif self.game.has_winner:
                self.highlight_cells()
                msg = f'Player "{self.game.current_player.label}" won!'
                color = self.game.current_player.color
                self.update_display(msg, color)
            else:
                self.game.next_player()
                msg = f"{self.game.current_player.label}'s turn"
                self.update_display(msg)


def main():
    """Create the game's board and run its main loop."""
    board = Board()
    board.mainloop()


if __name__ == "__main__":
    main()
