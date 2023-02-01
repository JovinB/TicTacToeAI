import tkinter as tk
from tkinter import font


class Board(tk.Tk):
    def __init__(self):
        super().__init__()
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
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )


def main():
    """Create the game's board and run its main loop."""
    board = Board()
    board.mainloop()


if __name__ == "__main__":
    main()
