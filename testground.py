import random
from game import Game, Move, Player
from minmax import MinMaxPlayer
from minmax_alphabeta import MinMaxAlphaBetaPlayer



g = Game()
g.print()

board = g.get_board()
print(board.shape)

# third column of board all ones the rest random numbers in 0, 1, -1

board[0, :] = [ 1, 1, 0, 0, 0]
board[1, :] =  [ 0, 1, 0, 0, 0]
board[2, :] =  [ 0, 1, 0, 0, 0]
board[3, :] =  [ 0, 1, 0, 1, 0]
board[4, :] =  [ 0, 1, 0, 0, 1]

print(board)
p = MinMaxAlphaBetaPlayer(3)
print(p.check_winner(board, 0))









# print(p.get_possible_moves(board, 0))
# # print(f"board score is :  {p.get_score(board, 20)}")





