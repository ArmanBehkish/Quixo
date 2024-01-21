import random
from game import Game, Move, Player

# MinMaxPlayer class inherited from Player class that implements the MinMax algorithm to play Quixo game (as defined in the Game class) and implements the abstract method make_move from Player class which receives the Game object and returns a tuple with the position of the piece to move and the direction to move it.
class MinMaxPlayer(Player):
    def __init__(self, depth: int) -> None:
        super().__init__()
        self.depth = depth

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:  
        board = game.get_board()
        player = game.get_current_player()
        best_move = self.minmax(board, player, self.depth)
        return best_move
    
    # MinMax algorithm that receives the board, the current player and the depth and returns the best move
    def minmax(self, board: list[list[int]], player: int, depth: int) -> tuple[tuple[int, int], Move]:

        possible_moves = self.get_possible_moves(board, player)
        if len(possible_moves) == 0:
            return None
        best_move = possible_moves[0]
        best_score = float('-inf')

        for move in possible_moves:
            # Get the new board after making the move
            new_board = self.make_move_board(board, move, player)
            # Get the score of the new board
            score = self.min(new_board, player, depth - 1)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move
    
    # Min algorithm that receives the board, the current player and the depth and returns the score of the board
    def min(self, board: list[list[int]], player: int, depth: int) -> int:
        # Get the possible moves from the board
        possible_moves = self.get_possible_moves(board, player)
        # If there are no possible moves, return the score of the board
        if len(possible_moves) == 0:
            return self.get_score(board, player)
        # Initialize the best score with the best possible score
        best_score = float('inf')
        # For each possible move
        for move in possible_moves:
            # Get the new board after making the move
            new_board = self.make_move_board(board, move, player)
            # Get the score of the new board
            score = self.max(new_board, player, depth - 1)
            # If the score is better than the best score
            if score < best_score:
                # Update the best score
                best_score = score
        # Return the best score
        return best_score
    
    # Max algorithm that receives the board, the current player and the depth and returns the score of the board
    def max(self, board: list[list[int]], player: int, depth: int) -> int:
        # Get the possible moves from the board
        possible_moves = self.get_possible_moves(board, player)
        # If there are no possible moves, return the score of the board
        if len(possible_moves) == 0:
            return self.get_score(board, player)
        # Initialize the best score with the worst possible score
        best_score = float('-inf')
        # For each possible move
        for move in possible_moves:
            # Get the new board after making the move
            new_board = self.make_move_board(board, move, player)
            # Get the score of the new board
            score = self.min(new_board, player, depth - 1)
            # If the score is better than the best score
            if score > best_score:
                # Update the best score
                best_score = score
        # Return the best score
        return best_score
    
    # Get the possible moves from the board
    # TESTED
    def get_possible_moves(self, board: list[list[int]], player: int) -> list[tuple[tuple[int, int], Move]]:
        possible_moves = []
        # len of ndarray returns the shape of the first dimension
        for row in range(len(board)):
            for col in range(len(board[row])):
                # If the piece belongs to the current player or is neutral
                if board[row][col] == player or board[row][col] == -1:
                    if row == 0:
                        if col == 0:
                            possible_moves.append(((row, col), Move.BOTTOM))
                            possible_moves.append(((row, col), Move.RIGHT))
                        if col == len(board[row]) - 1:
                            possible_moves.append(((row, col), Move.BOTTOM))
                            possible_moves.append(((row, col), Move.LEFT))
                        if col != 0 and col != len(board[row]) - 1:
                            possible_moves.append(((row, col), Move.BOTTOM))
                            possible_moves.append(((row, col), Move.LEFT))
                            possible_moves.append(((row, col), Move.RIGHT))
                    if row == len(board) - 1:
                        if col == 0:
                            possible_moves.append(((row, col), Move.TOP))
                            possible_moves.append(((row, col), Move.RIGHT))
                        if col == len(board[row]) - 1:
                            possible_moves.append(((row, col), Move.TOP))
                            possible_moves.append(((row, col), Move.LEFT))
                        if col != 0 and col != len(board[row]) - 1:
                            possible_moves.append(((row, col), Move.TOP))
                            possible_moves.append(((row, col), Move.LEFT))
                            possible_moves.append(((row, col), Move.RIGHT))
                    if row != 0 and row != len(board) - 1:
                        if col == 0:
                            possible_moves.append(((row, col), Move.TOP))
                            possible_moves.append(((row, col), Move.BOTTOM))
                            possible_moves.append(((row, col), Move.RIGHT))
                        if col == len(board[row]) - 1:
                            possible_moves.append(((row, col), Move.TOP))
                            possible_moves.append(((row, col), Move.BOTTOM))
                            possible_moves.append(((row, col), Move.LEFT))
        return possible_moves
    
    
    
    # player score: number of pieces on the board for the player
    def get_score(self, board: list[list[int]], player: int) -> int:
        score = 0
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == player:
                    score += 1
        return score
    

    # Get the new board after making the move
    def make_move_board(self, board: list[list[int]], move: tuple[tuple[int, int], Move], player: int) -> list[list[int]]:
        # Get the row and column of the piece to move
        row, col = move[0]
        # Get the direction to move the piece
        direction = move[1]
        # Initialize the new board
        new_board = []
        # For each row
        for r in range(len(board)):
            # Initialize the new row
            new_row = []
            # For each column
            for c in range(len(board[r])):
                # If the piece is in the row and column of the piece to move
                if r == row and c == col:
                    # If the direction is to move the piece up
                    if direction == Move.UP:
                        # Add the piece to the new row
                        new_row.append(board[r - 1][c])
                    # If the direction is to move the piece down
                    elif direction == Move.DOWN:
                        # Add the piece to the new row
                        new_row.append(board[r + 1][c])
                    # If the direction is to move the piece left
                    elif direction == Move.LEFT:
                        # Add the piece to the new row
                        new_row.append(board[r][c - 1])
                    # If the direction is to move the piece right
                    elif direction == Move.RIGHT:
                        # Add the piece to the new row
                        new_row.append(board[r][c + 1])
                # If the piece is not in the row and column of the piece to move
                else:
                    # Add the piece to the new row
                    new_row.append(board[r][c])
            # Add the new row to the new board
            new_board.append(new_row)
        # Return the new board
        return new_board

