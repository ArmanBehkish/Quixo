import random
from game import Game, Move, Player
from minmax import MinMaxPlayer



g = Game()
#g.print()

board = g.get_board()
print(board.shape)
# initialize the board the ndarray to all ones in first row and all 0 and 2 and 4 and all 1 in row 1 and 3
board[0, :] = 1
board[1, :] = 0
board[2, :] = 1
board[3, :] = 0
board[4, :] = -1
print(board)
print(type(board))
print(board[4,3])

# p = MinMaxPlayer(2)
# print(f"board score is :  {p.get_score(board, 20)}")





