import random

from game import Game, Move, Player
from minmax_alphabeta import MinMaxAlphaBetaPlayer
from minmax_alphabeta_2 import MinMaxAlphaBetaPlayer2
from interface import MatrixInterface
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication


class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(
        self, game: "Game", window: MatrixInterface
    ) -> tuple[tuple[int, int], Move]:
        # window.set_current_player("AI agent player")
        # window.update_display(game.get_board())
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def get_move(self, from_pos, new_click) -> Move:
        x_old, y_old = from_pos
        x, y = new_click
        move = Move.TOP

        # corner positions
        if x_old == 0 and y_old == 0:
            if x == 4 and y == 0:
                move = Move.RIGHT
            if x == 0 and y == 4:
                move = Move.BOTTOM
        if x_old == 4 and y_old == 0:
            if x == 0 and y == 0:
                move = Move.LEFT
            if x == 4 and y == 4:
                move = Move.BOTTOM
        if x_old == 0 and y_old == 4:
            if x == 0 and y == 0:
                move = Move.TOP
            if x == 4 and y == 4:
                move = Move.RIGHT
        if x_old == 4 and y_old == 4:
            if x == 0 and y == 4:
                move = Move.LEFT
            if x == 4 and y == 0:
                move = Move.TOP

        # non-corner positions
        if x_old in [1, 2, 3]:
            if y_old == 0:
                if x == 0:
                    move = Move.LEFT
                if x == 4:
                    move = Move.RIGHT
                if x in [1, 2, 3]:
                    move = Move.BOTTOM
            if y_old == 4:
                if x == 0:
                    move = Move.LEFT
                if x == 4:
                    move = Move.RIGHT
                if x in [1, 2, 3]:
                    move = Move.TOP

        if y_old in [1, 2, 3]:
            if x_old == 0:
                if y == 0:
                    move = Move.TOP
                if y == 4:
                    move = Move.BOTTOM
                if y in [1, 2, 3]:
                    move = Move.RIGHT
            if x_old == 4:
                if y == 0:
                    move = Move.TOP
                if y == 4:
                    move = Move.BOTTOM
                if y in [1, 2, 3]:
                    move = Move.LEFT

        return move

    def make_move(
        self, game: "Game", window: MatrixInterface
    ) -> tuple[tuple[int, int], Move]:

        window.set_current_player("Player")
        window.set_status("Waiting for Your move...")
        window.waiting_for_click = True
        while window.waiting_for_click:
            QApplication.processEvents()
        print("wait finsihed")
        x, y = window.last_clicked_button
        window.set_status(f"Position Selected ({x}, {y}), Choose direction...")
        from_pos = (x, y)
        window.waiting_for_click = True
        while window.waiting_for_click:
            QApplication.processEvents()
        print("second wait finsihed")
        x, y = window.last_clicked_button
        new_click = (x, y)
        move = self.get_move(from_pos, new_click)
        window.set_status(f"moving position {from_pos} to {move}")
        # move_input = int(input().strip())
        # move_input = random.randint(0, 3)
        # move = Move(move_input)
        return from_pos, move


if __name__ == "__main__":

    app = QApplication(sys.argv)
    g = Game()  # Create game instance outside the loop
    window = MatrixInterface(g.get_board())
    g.set_window(window)
    window.update_display(g.get_board())
    window.show()
    # sys.exit(app.exec_())
    player1 = MyPlayer()
<<<<<<< HEAD
    player2 = RandomPlayer()
    winner = g.play(player1, player2)
    g.print()
    print(f"Winner: Player {winner}")
    #HERE  Generating QR code for reward
    # Reward the winning player
    reward_amount = 10  # Set reward amount in sats
    g._reward_player(winner, reward_amount)
=======
    # player2 = MinMaxAlphaBetaPlayer(depth=3)
    player3 = MinMaxAlphaBetaPlayer2(depth=3)
    # p = RandomPlayer()
    winner = g.play(player1, player3)

    if winner == 0:
        window.set_status(f"Game Over! You win!")
    else:
        window.set_status(f"Game Over! Stupid AI wins!")

    # Wait for user action (close or restart)
    app.exec_()
>>>>>>> dac3ced (PyQt5 intf added)
