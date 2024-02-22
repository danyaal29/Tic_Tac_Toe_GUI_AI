import tkinter as tk
from tkinter import simpledialog, messagebox
import random
#Made by Danyaal Mubasher

# Minimax algorithm for AI decision-making
def minimax(board, depth, is_maximizing, ai_symbol, human_symbol):
    # Base cases: check for terminal states (win, lose, tie)
    if check_win(board, ai_symbol):
        return 10
    elif check_win(board, human_symbol):
        return -10
    elif check_tie(board):
        return 0

    # Maximizing player (AI)
    if is_maximizing:
        best_score = float('-inf')
        for r in range(3):
            for c in range(3):
                # Explore this move if the cell is empty
                if board[r][c] is None:
                    board[r][c] = ai_symbol  # Make the move
                    score = minimax(board, depth + 1, False, ai_symbol, human_symbol)  # Recurse with opponent's turn
                    board[r][c] = None  # Undo the move
                    best_score = max(score, best_score)
        return best_score
    # Minimizing player (opponent)
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] is None:
                    board[r][c] = human_symbol
                    score = minimax(board, depth + 1, True, ai_symbol, human_symbol)
                    board[r][c] = None
                    best_score = min(score, best_score)
        return best_score

# Find the best move for the AI player
def find_best_move(board, ai_symbol, human_symbol):
    best_score = float('-inf')
    move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] is None:
                board[r][c] = ai_symbol
                score = minimax(board, 0, False, ai_symbol, human_symbol)
                board[r][c] = None
                if score > best_score:
                    best_score = score
                    move = (r, c)
    return move

# Check if a player has won
def check_win(board, player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all([cell == player for cell in board[i]]) or all([board[j][i] == player for j in range(3)]):
            return True
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

# Check if the board is in a tie state (no empty spaces left)
def check_tie(board):
    for row in board:
        if None in row:
            return False
    return True

class TicTacToeGUI:
    def __init__(self):
        # Set up the main window
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        # Allow players to choose their symbols
        self.player_symbol, self.ai_symbol = self.ask_player_symbol()
        self.current_player = 'X'  # X starts the game
        # Initialize the game board data structure and GUI elements
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.initialize_board()

    # Prompt the player to choose a symbol
    def ask_player_symbol(self):
        choice = simpledialog.askstring("Tic Tac Toe", "Choose your symbol (X/O):")
        return ('O', 'X') if choice.upper() == 'O' else ('X', 'O')

    # Create and grid buttons for the game board
    def initialize_board(self):
        for r in range(3):
            for c in range(3):
                button = tk.Button(self.window, text='', font=('normal', 40), height=2, width=5,
                                   command=lambda r=r, c=c: self.on_click(r, c))
                button.grid(row=r, column=c)
                self.buttons[r][c] = button
        if self.current_player == self.ai_symbol:
            self.ai_turn()  # If AI plays first, make its move

    # Handle button click events
    def on_click(self, row, col):
        # Make a move if the cell is empty and the game isn't over
        if not self.board[row][col] and not self.check_game_over():
            self.board[row][col] = self.current_player  # Update the board
            self.buttons[row][col]['text'] = self.current_player  # Update the button text
            # Check for game over conditions
            if not self.check_game_over():
                # Switch turns
                self.current_player = self.ai_symbol if self.current_player == self.player_symbol else self.player_symbol
                if self.current_player == self.ai_symbol:
                    self.ai_turn()  # AI makes a move if it's its turn

    # AI player makes a move
    def ai_turn(self):
        move = find_best_move(self.board, self.ai_symbol, self.player_symbol)
        if move:
            self.on_click(*move)

    # Check for game over conditions (win or tie)
    def check_game_over(self):
        if check_win(self.board, self.current_player):
            messagebox.showinfo("Game Over", f"{self.current_player} wins!")
            self.reset_board()  # Reset the board for a new game
            return True
        if check_tie(self.board):
            messagebox.showinfo("Game Over", "It's a tie!")
            self.reset_board()
            return True
        return False
    #Made by Danyaal Mubasher

    # Reset the game board for a new game
    def reset_board(self):
        for r in range(3):
            for c in range(3):
                self.board[r][c] = None
                self.buttons[r][c]['text'] = ''
        self.current_player = 'X'
        if self.ai_symbol == 'X':
            self.ai_turn()  # If AI is 'X', it starts the new game

    # Start the game loop
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToeGUI()
    game.run()
