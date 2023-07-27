import tkinter as tk
from tkinter import messagebox

class TicTacToeGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.current_player = None
        self.board = [' '] * 9

        # Player choice window
        self.player_choice()

    def player_choice(self):
        choice_window = tk.Toplevel(self.root)
        choice_window.geometry("200x100")
        choice_window.title("Choose X or O")

        def choose_X():
            self.current_player = 'X'
            choice_window.destroy()
            self.create_board()

        def choose_O():
            self.current_player = 'O'
            choice_window.destroy()
            self.create_board()

        tk.Button(choice_window, text="X", font=('Helvetica', 24, 'bold'), command=choose_X).pack(side=tk.LEFT, padx=20)
        tk.Button(choice_window, text="O", font=('Helvetica', 24, 'bold'), command=choose_O).pack(side=tk.RIGHT, padx=20)

    def create_board(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.buttons = []
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text='', width=6, height=2, font=('Helvetica', 24, 'bold'),
                                command=lambda row=i, col=j: self.make_move(row, col))
                btn.grid(row=i, column=j)
                self.buttons.append(btn)

        self.play()

    def play(self):
        if self.current_player == 'O':
            self.computer_move()

    def make_move(self, row, col):
        index = row * 3 + col
        if self.board[index] == ' ':
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner(self.current_player):
                self.show_winner()
            elif ' ' not in self.board:
                self.show_draw()
            else:
                self.current_player = 'X' if self.current_player == 'O' else 'O'
                if self.current_player == 'O':
                    self.computer_move()

    def computer_move(self):
        best_score = float('-inf')
        best_move = None
        for i in range(len(self.board)):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i

        self.make_move(best_move // 3, best_move % 3)

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner('O'):
            return 1
        elif self.check_winner('X'):
            return -1
        elif ' ' not in board:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(len(board)):
                if board[i] == ' ':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(len(board)):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] == player:
                return True
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] == player:
                return True
        if self.board[0] == self.board[4] == self.board[8] == player:
            return True
        if self.board[2] == self.board[4] == self.board[6] == player:
            return True
        return False

    def show_winner(self):
        winner = "Player" if self.current_player == 'X' else "Computer"
        messagebox.showinfo("Game Over", f"{winner} wins!")
        self.ask_play_again()

    def show_draw(self):
        messagebox.showinfo("Game Over", "It's a draw!")
        self.ask_play_again()

    def ask_play_again(self):
        answer = messagebox.askyesno("Play Again", "Do you want to play again?")
        if answer:
            self.current_player = 'X' if self.current_player == 'O' else 'O'
            self.board = [' '] * 9
            self.create_board()
        else:
            self.root.quit()


if __name__ == "__main__":
    game = TicTacToeGame()
    game.root.mainloop()
