import tkinter as tk 
from tkinter import font


# Creating a  main class for the game, that inherits from tk.Tk to use tkinter window features
class TicTacToeBoard(tk.Tk):
    
    def __init__(self):
        super().__init__()   # Initlialize the parent class (tk.Tk)
        self.title("Tic Tac Toe")   # Window title 
        self._cells = {}  # Mapping between button widgets and their (row, col) coordinates
        self._create_board_display()  # Calling the display function which shows the game status
        self._board = [["" for _ in range(3)] for _ in range(3)]   # 3x3 game board initialized to empty
        self._create_board_grid() # Calling grid function to create button grid (the game board)
        self._game_over = False  # Tracking the game


    def _create_board_display(self):
        # Create a label at the top to show game status (turns, winner, tie)
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)  # Fill horizontally
        self.display = tk.Label(
            master=display_frame,
            text="New Game!", #  Initial game message
            font=font.Font(size=30, weight="bold"), 
        )
        self.display.pack() #  Show label on the screen


    def _create_board_grid(self):
        # Create 3x3 grid of buttons to represent the game board
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()  #  Display the grid frame
        for row in range(3):
            self.rowconfigure(row, weight=1, minsize=50)   # Resizing of rows
            self.columnconfigure(row, weight=1, minsize=75)   # Resizing of columns
            for col in range(3):
                #  Create each button representing a cell
                button = tk.Button(
                    master=grid_frame,
                    text="",  #  Initially empty
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="gray",
                    command=lambda r=row, c=col: self._handle_click(r, c)  # Call handler, on click
                )
                self._cells[button] = (row, col)  # Store the button´s position
                button.grid(
                    row=row,
                    column=col,
                    padx=4,
                    pady=4,
                    sticky="nsew"  #  Expand in all directions
                )

    def check_winner_on_board(self, board):
        # Check all rows for winner
        for row in board:
            if row[0] == row[1] == row[2] != "":
                return row[0]
        
        # Check for winner in columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != "":
                return board[0][col]
        
        # Check both diagonals
        if board[0][0] == board[1][1] == board[2][2] != "":
            return board[0][0]
        
        if board[0][2] == board[1][1] == board[2][0] != "":
            return board[0][2] 
        
        # No winners yet
        return None
    
    def _is_board_full(self):
        # Check if all cells are filled and return True if so
        for row in self._board:
            for cell in row:
                if cell == "":
                    return False
        return True
    
    def make_ai_move(self):
        # Let the AI make a move using the minimax algorithm
        if self._game_over:
            return
        
        move = self._find_best_move()  #  The optimal move for AI
        if move is None:
            return   # No move available
        
        row, col = move
        self._board[row][col] = "O"   #  Mark AI´s move on the board

        # Update corresponding GUI-button
        for button, (r, c) in self._cells.items():
            if r == row and c == col:
                button.config(text="O")
                break
        # Check for win/tie after AI move
        winner = self.check_winner_on_board(self._board)
        if winner:
            self._display_winner(winner)
            return
        elif self._is_board_full():
            self._display_winner(None)  # Tie 
            return
        
    def _find_best_move(self): 
        # Use minimax to find thre optimal move for AI (player 'O') 
        best_score = float('-inf')
        best_move = None

        for row in range(3):
            for col in range(3):
                if self._board[row][col] == "":  #  Only consider empty cells
                    self._board[row][col] = "O"  # AI makes move
                    score = self._minimax(self._board, 0, False)  # Evalute move
                    self._board[row][col] = ""  # Undo move
                    if score > best_score:  #  If the move is better, remember it
                        best_score = score
                        best_move = (row, col)
        return best_move 
    
    def _minimax(self, board, depth, is_maximizing):
        # Recursive function to evalute game states
        winner = self.check_winner_on_board(board)
        if winner == "O":
            return 10 - depth  #  AI wins, positive score
        elif winner == "X":
            return depth - 10  #  Player wins, negative score
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
                        board[row][col] = ""
                        best_score = min(score, best_score)
            return best_score
    
    def _display_winner(self, winner):
        # Update display and disable buttons
        if winner == "X" or winner == "O":
            self.display.config(text=f"Player {winner} Is The Winner!")
        else:
            self.display.config(text="It Is A Tie!")
        
        self._game_over = True  #  Stop future moves

        for button in self._cells:
            button.config(state=tk.DISABLED)

        self.after(3000, self.reset_board)  # Wait 3 seconds, then reset

    def _handle_click(self, row, col):
        # Handles player click on a button
        for button, (r, c) in self._cells.items():
            if r == row and c == col:
                if button["text"] == "" and not self._game_over:
                     # print(f"clicked at ({row}, {col})")
                    button.config(text="X")
                    self._board[row][col] = "X"
                    
                    #  Check for game result after player´s move
                    winner = self.check_winner_on_board(self._board)
                    if winner:
                        self.display.config(text=f"Player {winner} Is The Winner!")
                        self._game_over = True
                        self.after(3000, self.reset_board)
                        return
                    elif self._is_board_full():
                        self.display.config(text="It Is A Tie!")
                        self._game_over = True
                        self.after(3000, self.reset_board)
                        return
                    
                    # Let AI make a move after a short delay
                    self.after(300, self.make_ai_move)
                break

    
    def reset_board(self):
        # Clear the board and reset the game state
        for button in self._cells:
            button.config(text="", state=tk.NORMAL)  # Clear the buttons
        self._board = [["" for _ in range(3)] for _ in range(3)]  # Emtpies the game logic board
        self._player_turn = True # Let player X starts always
        self._game_over = False  #  The game is ongoing
        self.display.config(text="New Game!")  #  Update status display
    
# Function for running the whole program
def main():
    board = TicTacToeBoard()  # Instance of the game
    board.mainloop()   # starts Tkinter main loop

# Run game if this file is the main program
if __name__ == "__main__":
    main()

