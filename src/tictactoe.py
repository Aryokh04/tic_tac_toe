import tkinter as tk 
from tkinter import font

# Creating a class that inherits from tk.Tk to use tkinter methods
class TicTacToeBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self._cells = {}

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.label(
            master=display_frame,
            text="ready?",
            font=font.Font(size=30, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame 

