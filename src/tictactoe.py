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
        self._player_turn = True  # True = player X, False = player O (AI)
        self._board = [["" for _ in range(3)] for _ in range(3)]   # Empty board 


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

    def check_winner_on_board(self, board):
        # Check for 3 of same symbols un rows
        for row in board:
            if row[0] == row[1] == row[2] != "":
                return row[0]
        
        # Check for winner in columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != "":
                return board[0][col]
        
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != "":
            return board[0][0]
        
        if board[0][2] == board[1][1] == board[2][0] != "":
            return board[0][2] 
        
        # No winners
        return None
    
    def is_board_full(self):
        for row in self._board:
            for cell in row:
                if cell == "":
                    return False
        return True


    def _handle_click(self, row, col, button):
        if button["text"] == "" and not self._game_over:
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
                self.reset_board
                return
            
        self.after(300, self.make_ai_move)
    
    def reset_board(self):
        for button in self._cells:
            button.config(text="", state=tk.NORMAL)
        self._board = [["" for _ in range(3)] for _ in range(3)]
        self._player_turn = True 
        self._game_over = False 
        self.display.config(text="New Game! X goes first")
    
   
def main():
    board = TicTacToeBoard()  # Instance of the class
    board.mainloop()   # opens and keeps the window running

if __name__ == "__main__":
    main()

