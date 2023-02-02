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
        self.create_menu()
        self.create_main_window()
        self.create_board()

    def create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(
            label="Play Again",
            command=self.reset_board
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

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

    def update_button(self, button):
        button.config(text=self.game.current_player.label)
        button.config(fg=self.game.current_player.colour)

    def update_display(self, msg, colour="black"):
        self.display["text"] = msg
        self.display["fg"] = colour

    def highlight_cells(self):
        for button, coordinates in self.tiles.items():
            if coordinates in self.game.winner_combo:
                button.config(highlightbackground="red")

    def play(self, event):
        button = event.widget
        row, col = self.tiles[button]
        move = Move(row, col, self.game.current_player.label)
        if self.game.is_move_valid(move):
            self.update_button(button)
            self.game.perform_action(move)
            if self.game.is_tied():
                self.update_display(msg="Tied game!", colour="red")
            elif self.game.has_winner:
                self.highlight_cells()
                msg = f'Player "{self.game.current_player.label}" won!'
                colour = self.game.current_player.colour
                self.update_display(msg, colour)
            else:
                self.game.next_player()
                self.ai_turn()

    def ai_turn(self):
        move = self.game.ai_move()
        button = [b for b, coords in self.tiles.items() if coords == (move.row, move.col)][0]
        self.update_button(button)

        if self.game.is_tied():
            self.update_display(msg="Tied game!", colour="red")
        elif self.game.has_winner:
            self.highlight_cells()
            msg = f'Player "{self.game.current_player.label}" won!'
            colour = self.game.current_player.colour
            self.update_display(msg, colour)
        else:
            self.game.next_player()

    def reset_board(self):
        self.game.reset_game()
        self.update_display(msg="Ready?")
        for button in self.tiles.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")
