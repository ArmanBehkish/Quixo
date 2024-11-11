import random
from game import Game, Move, Player


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


if __name__ == '__main__':
    g = Game()
    g.print()
    player1 = MyPlayer()
    player2 = RandomPlayer()
    winner = g.play(player1, player2)
    g.print()
    print(f"Winner: Player {winner}")
    #HERE  Generating QR code for reward
    # Reward the winning player
    reward_amount = 10  # Set reward amount in sats
    g._reward_player(winner, reward_amount)
