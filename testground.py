import random
from game import Game, Move, Player
from minmax import MinMaxPlayer



g = Game()
g.print()

board = g.get_board()
print(board.shape)

board[0, :] = 1
board[1, :] = 0
board[2, 0:3] = 10
board[3, :] = 0
board[4, :] = -1
print(board)
print(board[2,1:])



# p = MinMaxPlayer(4)
# print(p.get_possible_moves(board, 0))
# # print(f"board score is :  {p.get_score(board, 20)}")





