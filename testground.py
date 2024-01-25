import random
from game import Game, Move, Player
from minmax import MinMaxPlayer



g = Game()
g.print()

board = g.get_board()
print(board.shape)

board[0, :] = [-1, 1, 1, 0, 0]
board[1, :] =  [ 1, 0, 0, 0, 0]
board[2, :] = [-1, 0, 0, -1, -1]
board[3, :] = [ 0, 0, -1, -1, 1]
board[4, :] = [-1, 1, -1, 0, -1]
print(board)
p = MinMaxPlayer(3)
print(p.get_possible_moves(board, 1))







# print(p.get_possible_moves(board, 0))
# # print(f"board score is :  {p.get_score(board, 20)}")





