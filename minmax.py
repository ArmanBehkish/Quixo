from copy import deepcopy
import random
from game import Game, Move, Player

class MinMaxPlayer(Player):
    def __init__(self, depth: int) -> None:
        super().__init__()
        self.depth = depth
        self.agent = "MinMax Agent"

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:  
        self._game = game
        board = game.get_board()
        player = game.get_current_player()
        self._maximizer_player = player
        self._minimizer_player = 1 - player
        best_move = self.minmax(board, player, self.depth)
        return best_move
    

    def minmax(self, board: list[list[int]], player: int, depth: int) -> tuple[tuple[int, int], Move]:

        possible_moves = self.get_possible_moves(board, player)

        # terminal node check
        if depth == 0 or self.check_winner(board,player) != -1 or possible_moves == None:
            return self.get_score(board, player)

        # here mini player
        if player == self._minimizer_player:
            value = float('inf')
            best_move = possible_moves[0]
            for move in possible_moves:
                new_board = self.make_move_board(board, move, player)
                # original player was assumed as maxplayer, so here we pass the minplayer
                score = self.minmax(new_board, 1 - player, depth - 1) 
                # take minimum score of childs
                if score < value:
                    value = score
                    best_move = move

        # here max player
        if player == self._maximizer_player:
            value = float('-inf')
            best_move = possible_moves[0]
            for move in possible_moves:
                new_board = self.make_move_board(board, move, player)
                # original player was assumed as maxplayer, so here we pass the minplayer
                score = self.minmax(new_board, 1 - player, depth - 1)
                # take the maximum score of childs
                if score > value:
                    value = score
                    best_move = move

        return best_move
 

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
    # TESTED
    def get_score(self, board: list[list[int]], player: int) -> int:
        score = 0

        if player != 1 and player != 0:
            raise ValueError("player must be 0 or 1")
        
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == player:
                    score += 1
        return score

    


    def make_move_board(self, board: list[list[int]], move: tuple[tuple[int, int], Move], player: int) -> list[list[int]]:
        '''Get the new board after making the move; same logic as the GAME class'''

        # inside all function I use row, col coordinates; I will switch places in the final return value of the agent move.
        # passed move
        row, col = move[0]
        direction = move[1]

        if player > 2:
            raise ValueError("player must be 0 or 1")
        
        #prev_value = deepcopy(board[(row, col)])
        acceptable, board = self.take((row, col), player, board)
        if acceptable:
            acceptable,new_board = self.slide((row, col), direction, board)
            if not acceptable:
                raise ValueError(f"slide tried in the {self.agent} is not acceptable!")
            return new_board
        raise ValueError(f"piece taken in the {self.agent} is not acceptable!")


    def take(self, from_pos: tuple[int, int], player_id: int, board: list[list[int]]) -> bool:
        '''Take piece'''
        # acceptable only if in border
        acceptable: bool = (
            # check if it is in the first row
            (from_pos[0] == 0 and from_pos[1] < 5)
            # check if it is in the last row
            or (from_pos[0] == 4 and from_pos[1] < 5)
            # check if it is in the first column
            or (from_pos[1] == 0 and from_pos[0] < 5)
            # check if it is in the last column
            or (from_pos[1] == 4 and from_pos[0] < 5)
            # and check if the piece can be moved by the current player
        ) and (board[from_pos] < 0 or board[from_pos] == player_id)
        if acceptable:
            board[from_pos] = player_id
        return acceptable, board

    def slide(self, from_pos: tuple[int, int], slide: Move, board: list[list[int]] ) -> bool:
        '''Slide the other pieces'''
        # define the corners
        SIDES = [(0, 0), (0, 4), (4, 0), (4, 4)]
        # if the piece position is not in a corner
        if from_pos not in SIDES:
            acceptable_top: bool = from_pos[0] == 0 and (
                slide == Move.BOTTOM or slide == Move.LEFT or slide == Move.RIGHT
            )
            acceptable_bottom: bool = from_pos[0] == 4 and (
                slide == Move.TOP or slide == Move.LEFT or slide == Move.RIGHT
            )
            acceptable_left: bool = from_pos[1] == 0 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.RIGHT
            )
            acceptable_right: bool = from_pos[1] == 4 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.LEFT
            )
        # if the piece position is in a corner
        else:
            acceptable_top: bool = from_pos == (0, 0) and (
                slide == Move.BOTTOM or slide == Move.RIGHT)
            acceptable_left: bool = from_pos == (4, 0) and (
                slide == Move.TOP or slide == Move.RIGHT)
            acceptable_right: bool = from_pos == (0, 4) and (
                slide == Move.BOTTOM or slide == Move.LEFT)
            acceptable_bottom: bool = from_pos == (4, 4) and (
                slide == Move.TOP or slide == Move.LEFT)
            
        # check if the move is acceptable
        acceptable: bool = acceptable_top or acceptable_bottom or acceptable_left or acceptable_right
        # if it is
        if acceptable:
            # take the piece
            piece = board[from_pos]
            if slide == Move.LEFT:
                # for each column starting from the column of the piece and moving to the left
                for i in range(from_pos[1], 0, -1):
                    # copy the value contained in the same row and the previous column
                    board[(from_pos[0], i)] = board[(
                        from_pos[0], i - 1)]
                # move the piece to the left
                board[(from_pos[0], 0)] = piece
            # if the player wants to slide it to the right
            elif slide == Move.RIGHT:
                # for each column starting from the column of the piece and moving to the right
                for i in range(from_pos[1], board.shape[1] - 1, 1):
                    # copy the value contained in the same row and the following column
                    board[(from_pos[0], i)] = board[(
                        from_pos[0], i + 1)]
                # move the piece to the right
                board[(from_pos[0], board.shape[1] - 1)] = piece
            # if the player wants to slide it upward
            elif slide == Move.TOP:
                # for each row starting from the row of the piece and going upward
                for i in range(from_pos[0], 0, -1):
                    # copy the value contained in the same column and the previous row
                    board[(i, from_pos[1])] = board[(
                        i - 1, from_pos[1])]
                # move the piece up
                board[(0, from_pos[1])] = piece
            # if the player wants to slide it downward
            elif slide == Move.BOTTOM:
                # for each row starting from the row of the piece and going downward
                for i in range(from_pos[0], board.shape[0] - 1, 1):
                    # copy the value contained in the same column and the following row
                    board[(i, from_pos[1])] = board[(
                        i + 1, from_pos[1])]
                # move the piece down
                board[(board.shape[0] - 1, from_pos[1])] = piece
        return acceptable,board
    


    def check_winner(self, board: list[list[int]],player: int) -> int:
        '''Check if there is a winner,
        why the winner should not be the current player?'''

     # for each row
        winner = -1
        for x in range(board.shape[0]):
            # if a player has completed an entire row
            if board[x, 0] != -1 and all(board[x, :] == board[x, 0]):
                # return winner is this guy
                winner = board[x, 0]
        #if winner > -1 and winner != player:
        if winner > -1:
            return winner
        # for each column
        for y in range(board.shape[1]):
            # if a player has completed an entire column
            if board[0, y] != -1 and all(board[:, y] == board[0, y]):
                # return the relative id
                winner = board[0, y]
        #if winner > -1 and winner != player:
        if winner > -1:
            return winner
        # if a player has completed the principal diagonal
        if board[0, 0] != -1 and all(
            [board[x, x]
                for x in range(board.shape[0])] == board[0, 0]
        ):
            # return the relative id
            winner = board[0, 0]
        #if winner > -1 and winner != self.get_current_player():
        if winner > -1:
            return winner
        # if a player has completed the secondary diagonal
        if board[0, -1] != -1 and all(
            [board[x, -(x + 1)]
             for x in range(board.shape[0])] == board[0, -1]
        ):
            # return the relative id
            winner = self._board[0, -1]
        return winner

    def play(self, player1: Player, player2: Player) -> int:
        '''Play the game. Returns the winning player'''
        players = [player1, player2]
        winner = -1
        while winner < 0:
            self.current_player_idx += 1
            self.current_player_idx %= len(players)
            ok = False
            while not ok:
                from_pos, slide = players[self.current_player_idx].make_move(
                    self)
                ok = self.__move(from_pos, slide, self.current_player_idx)
                print(f'current game state is :\n {self._board} \n ok state is {ok}')
 
            winner = self.check_winner()
        return winner