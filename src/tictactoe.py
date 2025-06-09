import tkinter as tk 
from tkinter import font


# Creating a class that inherits from tk.Tk to use tkinter methods
class TicTacToeBoard(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self._cells = {}
        self._create_board_display()
        self._board = [["" for _ in range(3)] for _ in range(3)]   # Empty board 
        self._create_board_grid()
        self._player_turn = True  # True = player X, False = player O (AI)
        self._game_over = False 


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
                    command=lambda r=row, c=col, b=button: self._handle_click(r, c, b)
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
    
    def _is_board_full(self):
        for row in self._board:
            for cell in row:
                if cell == "":
                    return False
        return True
    
    def make_ai_move(self):
        if self._game_over:
            return
        
        move = self._find_best_move()
        if move is None:
            return
        
        row, col = move
        self._board[row][col] = "O"

        # Update GUI-button
        for button, (r, c) in self._cells.items():
            if r == row and c == col:
                button.config(text="O")
                break
        
        winner = self.check_winner_on_board(self._board)
        if winner:
            self._display_winner(winner)
            return
        elif self._is_board_full():
            self._display_winner(None)  # Tie 
            return
        
    def _find_best_move(self): 
        best_score = float('-inf')
        best_move = None

        for row in range(3):
            for col in range(3):
                if self._board[row][col] == "":
                    self._board[row][col] = "O"  # AI makes tentative move
                    score = self._minimax(self._board, 0, False)
                    self._board[row][col] = ""  # Undo move
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        return best_move 
    
    def _minimax(self, board, depth, is_maximizing):
        winner = self.check_winner_on_board(board)
        if winner == "O":
            return 10 - depth
        elif winner == "X":
            return depth - 10
        elif self._is_board_full():
            return 0  # Tie 
        
        if is_maximizing:
            best_score = float('-inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == "":
                        board[row][col] = "O"
                        score = self._minimax(board, depth + 1, False)
                        board[row][col] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == "":
                        board[row][col] = "X"
                        score = self._minimax(board, depth + 1, True)
                        board[row][col = ""
                        best_score = min(score, best_score)
            return best_score
    
    

    def _handle_click(self, row, col, button):
        if button["text"] == "" and not self._game_over:
            print(f"clicked at ({row}, {col})")  # test
            button.config(text="X")
            self._board[row][col] = "X"

            winner = self.check_winner_on_board(self._board)
            if winner:
                self.display.config(text=f"Player {winner} Is The Winner!")
                self._game_over = True 
                self.after(3000, self.reset_board) # Reset board after 3 seconds
                return 
            elif self._is_board_full():
                self.display.config(text="It Is A Tie!")
                self._game_over = True
                self.after(3000, self.reset_board)  # Reset board after 3 seconds
                return
            
        self.after(300, self.make_ai_move)
    
    def reset_board(self):
        for button in self._cells:
            button.config(text="", state=tk.NORMAL)  # Empty the buttons and activate them
        self._board = [["" for _ in range(3)] for _ in range(3)]  # Emtpies the board
        self._player_turn = True # Let player X start
        self._game_over = False  #  The game is not over
        self.display.config(text="New Game! X goes first")  #  Update display
    
   
def main():
    board = TicTacToeBoard()  # Instance of the class
    board.mainloop()   # opens and keeps the window running

if __name__ == "__main__":
    main()

