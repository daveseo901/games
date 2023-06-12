import os
from time import sleep
import numpy as np

class Board:
    symbols = {0: 'X', 1: 'O'}

    def __init__(self):
        self.board = [[' ' for i in range(3)] for j in range(3)]

    def get_move(self):
        while True:
            sleep(0.3)
            user_in = input('move?\n').split()
            user_in = list(map(int, user_in))
            if len(user_in) != 2:
                print("invalid move: 1 row and 1 column expected")
            elif min(user_in) < 0 or max(user_in) > 2:
                print("invalid move: 1 row and 1 column expected")
            elif self.board[user_in[0]][user_in[1]] != ' ':
                print("invalid move: space occupied")
            else:
                break
        return user_in[0], user_in[1]

    def make_move(self, row, col, player):
        self.board[row][col] = self.symbols[player]

    def is_win(self, row, col):
        vecs = np.array([[1, 1], [0, 1], [1, 0], [1, -1]])
        symbol = self.board[row][col]
        for vec in vecs:
            first_pos = np.array([row, col])
            for i in range(3):
                pos = (first_pos + i * vec) % 3
                if vec[0] * vec[1] == 1 and tuple(pos) == (0, 2):
                    break
                if vec[0] * vec[1] == -1 and tuple(pos) == (0, 0):
                    break
                if self.board[pos[0]][pos[1]] != symbol:
                    break
                elif i == 2:
                    return True
        return False

    def print_board(self):
        os.system('clear')
        div = '---' + '|---' * 2
        for ind, row in enumerate(self.board):
            line = ' ' + ' | '.join(row)
            print(line)
            if ind < 2:
                print(div)

def tictactoe():
    board = Board()
    in_prog = True
    player = 0
    sleep(0.1)
    while True:
        board.print_board()
        row, col = board.get_move()
        board.make_move(row, col, player)
        sleep(0.1)
        if board.is_win(row, col):
            board.print_board()
            print("player " + board.symbols[player] + " wins!")
            break
        player = (player + 1) % 2
    return 0

def main():
    tictactoe()

if __name__ == "__main__":
    main()
