# Tic Tac Toe with AI

Tic Tac Toe game with a graphical user interface (GUI) made using Python´s Tkinter library. The game allows a human player to play against an AI oppononent created with the Minimax algorithm, leading to either impossible wins or tie. 

**Features**
- 3x3 Tic Tac Toe grid
- Human player as x, AI as O
- AI uses the Minimax algorithm
- Gamer displays messages for: 
  - Player status
  - Winner announcement
  - Tie match
- Automatic reset after game ends with a 3 seconds delay
- Disabling button when game is over to prevent further input

**Running the program**
- Run "python3 tictactoe.py"
- GUI will show the game board
- Click empty cells to make a move, and AI will respond immediately
- When game ends, the board resets

**How it works**
- Human player alwasy goes first (X)
- The AI uses the Minimax algorithm for determining the best move
- The program checks for wins or ties 
- Once the game is ended, all buttons are disabled and the result is displayed 
- After 3 seconds, game resets 