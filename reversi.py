import os
from time import sleep
import numpy as np

class Board:
    symbols = {0: 'B', 1: 'W'}
    player = 0
    pieces = [set(), set()]
    moves = set()
    no_move = False # True if opponent's previous turn had no moves
    dim = 8 # width of board (assumes square board)

    def __init__(self, start=[[(3,4),(4,3)],[(3,3),(4,4)]]):
        self.board = [[' ' for i in range(self.dim)] for j in range(self.dim)]
        for i in range(2):
            symbol = self.symbols[i]
            for piece in start[i]:
                if len(piece) != 2:
                    print("error: piece must have two coordinates")
                    return
                if min(piece) < 0 or max(piece) >= self.dim:
                    print("error: piece " + str(piece) + " not within bounds")
                    return
                self.board[piece[0]][piece[1]] = symbol
                self.pieces[i].add(tuple(piece))
                
    def get_valid_moves(self):
        self.moves = set()
        vecs = np.array([-1,1,-1,0,1,1,0,-1,-1])
        for piece in self.pieces[self.player]:
            pos = np.array(piece)
            symbol = self.symbols[self.player]
            other_symbol = self.symbols[(self.player + 1) % 2]
            for i in range(self.dim):
                vec = vecs[i:i+2]
                cur_pos = pos + vec
                while min(cur_pos) >= 0 and max(cur_pos) < self.dim and \
                 self.board[cur_pos[0]][cur_pos[1]] == other_symbol:
                    cur_pos += vec
                if self.board[cur_pos[0] - vec[0]][cur_pos[1] - vec[1]] != other_symbol:
                    continue
                if min(cur_pos) >= 0 and max(cur_pos) < self.dim and \
                 self.board[cur_pos[0]][cur_pos[1]] == ' ':
                    self.moves.add(tuple(cur_pos))
        for ind, move in enumerate(self.moves):
            self.board[move[0]][move[1]] = str(ind + 1)

    def get_user_move(self):
        move_list = list(self.moves)
        quit_message = "enter the number for your move\nor enter <q> to quit\n"
        prompt = self.symbols[self.player] + "'s turn\navailable moves:\n" + \
         '\n'.join(['{0}) {1}'.format(i + 1, move_list[i]) for i in range(len(self.moves))]) + \
         '\n' + quit_message
        if len(self.moves) == 0:
            prompt = 'no moves available, enter anything to continue\n' + quit_message
            user_in = input(prompt)
            if user_in == 'q':
                return user_in
            return None
        while True:
            sleep(0.3)
            user_in = input(prompt)
            if user_in == 'q':
                return user_in
            if len(user_in) == 0:
                print("invalid move: choose one of the available moves")
                continue
            user_in = int(user_in)
            if user_in < 1 or user_in > len(self.moves):
                print("invalid move: choose one of the available moves")
            else:
                break
        return move_list[user_in - 1]

    def make_move(self, move):
        if move == None:
            return

        self.board[move[0]][move[1]] = self.symbols[self.player]
        self.pieces[self.player].add(move)

        # flip opponent tiles
        vecs = np.array([-1,1,-1,0,1,1,0,-1,-1])
        pos = np.array(move)
        symbol = self.symbols[self.player]
        other_symbol = self.symbols[(self.player + 1) % 2]
        for i in range(8):
            vec = vecs[i:i+2]
            cur_pos = pos + vec
            while min(cur_pos) >= 0 and max(cur_pos) < self.dim and \
             self.board[cur_pos[0]][cur_pos[1]] == other_symbol:
                cur_pos += vec
            if min(cur_pos) < 0 or max(cur_pos) >= self.dim:
                continue
            if self.board[cur_pos[0]][cur_pos[1]] != symbol or \
             self.board[cur_pos[0] - vec[0]][cur_pos[1] - vec[1]] != other_symbol:
                continue
            cur_pos -= vec
            while self.board[cur_pos[0]][cur_pos[1]] == other_symbol:
                self.board[cur_pos[0]][cur_pos[1]] = symbol
                self.pieces[(self.player + 1) % 2].remove(tuple(cur_pos))
                self.pieces[self.player].add(tuple(cur_pos))
                cur_pos -= vec

        for move in self.moves:
            if self.board[move[0]][move[1]] != self.symbols[self.player]:
                self.board[move[0]][move[1]] = ' '

    def is_win(self, move):
        return self.no_move and move == None
    
    def print_board(self):
        os.system('clear')
        border = "REVERSI!"
        header = '  ' + '   '.join([*border]) + '  '
        print(header)
        div = ' ---' + '|---' * (self.dim - 1)
        for ind, row in enumerate(self.board):
            line = border[::-1][ind]
            for i in range(self.dim):
                if len(row[i]) < 2:
                    line += ' '
                line += row[i]
                if i < self.dim - 1:
                    line += ' |'
            line += ' ' + border[ind]
            print(line)
            if ind < self.dim - 1:
                print(div)
        print(header[::-1])

def reversi():
    board = Board()
    in_prog = True
    player = 0
    sleep(0.1)
    while True:
        board.get_valid_moves()
        board.print_board()
        move = board.get_user_move()
        if move == 'q':
            return 1
        board.make_move(move)
        sleep(0.1)
        if board.is_win(move):
            board.print_board()
            scores = [len(group) for group in board.pieces]
            if scores[0] == scores[1]:
                print("it's a tie!")
            else:
                print("player " + board.symbols[np.argmax(scores)] + " wins!")
                for i in range(2):
                    print(board.symbols[i] + "'s score: " + str(scores[i]))
            break
        if move == None:
            board.no_move = True
        else:
            board.no_move = False
        board.player = (board.player + 1) % 2
    return 0

def main():
    reversi()

if __name__ == "__main__":
    main()
