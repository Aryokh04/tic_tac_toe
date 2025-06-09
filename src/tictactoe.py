import tkinter as tk 
from tkinter import font

# Creating a class that inherits from tk.Tk to use tkinter methods
class TicTacToeBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self._cells = {}
        self._create_board_display()
        self._create_board_grid()

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Start!",
            font=font.Font(size=30, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
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
                    highlightbackground="gray",
                )
                self._cells[button] = (row, col)
                button.grid(
                    row=row,
                    column=col,
                    padx=4,
                    pady=4,
                    sticky="nsew"
                )

    def _handle_click(self, row, col, button):
        if button["text"] == self._game_over:
            button.config(text="X")
            self._board[row][col] = "O"

            winner = self.check_winner_on_board(self._board)
            if winner:
                self.display.config(text=f"Player {winner} Is The Winner!")
                self._disable_buttons()
                self._game_over = True 
                return 
            elif self.is_board_full():
                self.display.config(text="It Is A Tie!")
                self._game_over = True 
                return
            
        self.after(300, self.make_ai_move)
    
   
def main():
    board = TicTacToeBoard()  # Instance of the class
    board.mainloop()   # opens and keeps the window running

if __name__ == "__main__":
    main()

