import random
from game import Game, Move, Player
from minmax import MinMaxPlayer


class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move
    
class ManualPlayer(Player):
    '''A manual player to test the workings of the game'''
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:

        col = int(input("Enter a col number between 0 and 4: "))
        row = int(input("Enter a row number between 0 and 4: "))
        direction = input("Enter a direction in top,bottom,left, right: ")

        from_pos = (col,row)
        if direction == "top":
            move = Move.TOP
        elif direction == "bottom":
            move = Move.BOTTOM
        elif direction == "left":
            move = Move.LEFT
        elif direction == "right":
            move = Move.RIGHT

        print(f"selected position : {from_pos} direction : {move}")
        return from_pos, move

if __name__ == '__main__':
    g = Game()
    g.print()
    #player1 = ManualPlayer()
    player1 = MinMaxPlayer(4)
    player2 = RandomPlayer()
    winner = g.play(player1, player2)
    g.print()
    print(f"Winner: Player {winner}")
