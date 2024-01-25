import random
import sys
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

    #sys.setrecursionlimit(100000)
    number_of_games = 20
    count = 0
    number_of_wins = {0: 0, 1: 0}
    agent = "MinMaxPlayer"

    for x in range(number_of_games):
        g = Game()
        #g.print()
        #player1 = ManualPlayer()
        player1 = MinMaxPlayer(3)
        player2 = RandomPlayer()
        winner = g.play(player2, player1)
        number_of_wins[winner] += 1
        count += 1
        #g.print()
        print(f"Player {winner}: number of games played: {count} and number of wins: {number_of_wins[winner]}")

    print(f" {agent} won {number_of_wins[1]} times")
