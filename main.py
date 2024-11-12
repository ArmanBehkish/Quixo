import random
from typing import Optional
from game import Game, Move, Player
from minmax_alphabeta import MinMaxAlphaBetaPlayer
from minmax_alphabeta_2 import MinMaxAlphaBetaPlayer2
from interface import MatrixInterface
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication
from variables import *
from zbd import zbd
import qrcode
import time


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
        move: Optional[Move] = None

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
                # first row
                if x == 0:
                    move = Move.LEFT
                if x == 4:
                    move = Move.RIGHT
                if x == x_old:
                    move = Move.BOTTOM
            if y_old == 4:
                # last row
                if x == 0:
                    move = Move.LEFT
                if x == 4:
                    move = Move.RIGHT
                if x == x_old:
                    move = Move.TOP

        if y_old in [1, 2, 3]:
            if x_old == 0:
                # first column
                if y == 0:
                    move = Move.TOP
                if y == 4:
                    move = Move.BOTTOM
                if y == y_old:
                    move = Move.RIGHT
            if x_old == 4:
                # last column
                if y == 0:
                    move = Move.TOP
                if y == 4:
                    move = Move.BOTTOM
                if y == y_old:
                    move = Move.LEFT

        if move is None:
            raise ValueError(f"No move found for {from_pos} to {new_click}")
        return move

    def make_move(
        self, game: "Game", window: MatrixInterface
    ) -> tuple[tuple[int, int], Move]:

        window.set_current_player("Player")
        window.set_status("Waiting for Your move...")
        window.waiting_for_click = True
        while window.waiting_for_click:
            QApplication.processEvents()
        x, y = window.last_clicked_button
        window.set_status(f"Position Selected ({x}, {y}), Choose direction...")
        from_pos = (x, y)
        window.waiting_for_click = True
        while window.waiting_for_click:
            QApplication.processEvents()
        x, y = window.last_clicked_button
        new_click = (x, y)
        move = self.get_move(from_pos, new_click)
        window.set_status(f"moving position {from_pos} to {move}")
        return from_pos, move


if __name__ == "__main__":
    zbd_client = zbd(apikey=ZEBEDEE_API_KEY)

    #HERE Preliminary tests #
    # Validate the Lightning address
    try:
        zbd_client.validate_lightning_address(ZEBEDEE_LIGHTNING_ADDRESS)
        print(f"Lightning address {ZEBEDEE_LIGHTNING_ADDRESS} is valid.")
    except Exception as e:
        print(f"Error validating Lightning address: {e}")
        exit(1)

    # Get wallet details
    try:
        wallet_details = zbd_client.get_wallet_details()
        print(f"Wallet details: {wallet_details}")

        # Ensure wallet balance is over REWARD_AMOUNT
        wallet_balance = wallet_details.get('balance', 0)
        if float(wallet_balance) >= REWARD_AMOUNT:
            print(f"Wallet balance {wallet_balance} is over the reward amount {REWARD_AMOUNT}.")
        else:
            print(f"Wallet balance {wallet_balance} is below the reward amount {REWARD_AMOUNT}.")
    except Exception as e:
        print(f"Error getting wallet details: {e}")
        exit(1)

    #HERE Payment wall #
    # Generate paywall
    charge_response = zbd_client.create_charge(
        amount_of_seconds_to_expire_after=INVOICE_EXPIRY,
        amount_msats=PAYWALL_AMOUNT,  # Example amount >=1000 and /1000
        description="Pay to start the game",
    )
    charge_id = charge_response["id"]
    charge_details = zbd_client.get_charge_details(charge_id)
    lightning_invoice = charge_details["invoice"]["request"]

    print("Please pay the following invoice to start the game:")
    qr = qrcode.make(lightning_invoice)
    qr.save("paywall_qr.png")
    print(f"QR Code saved as paywall_qr.png")
    print(f"Lightning Invoice: {lightning_invoice}")
    # HERE Wait for payment confirmation (simplified for demonstration) #
    # HACK To avoid payment
    input("Press Enter after payment...")

    # HERE Generate Pyqt window #
    app = QApplication(sys.argv)
    g = Game()
    window = MatrixInterface(g.get_board())
    g.set_window(window)
    window.update_display(g.get_board())

    window.show()

    # HERE Game definition #
    player1 = MyPlayer()
    player2 = MinMaxAlphaBetaPlayer2(depth=int(window.ai_search_depth))

    winner = g.play(player1, player2)

    if winner == 0:
        window.set_status(f"Game Over! You win!")
    else:
        window.set_status(f"Game Over! Stupid AI wins!")

    # HERE Generate withdrawal request for the winner #
    reward_description = PLAYER_REWARD_DESCRIPTION_TEMPLATE.format(winner_id=winner)
    withdrawal_response = zbd_client.create_withdrawal_request(
        amount_of_seconds_to_expire_after=INVOICE_EXPIRY,
        amount_msats=REWARD_AMOUNT,
        description="Got your reward",
        internal_id="11af01d092444a317cb33faa6b8304b8",
    )

    withdrawal_id = withdrawal_response["id"]
    withdrawal_details = zbd_client.get_withdrawal_request_details(withdrawal_id)
    withdrawal_invoice = withdrawal_details["invoice"]["request"]

    print("Congratulations! Here is your reward:")
    qr = qrcode.make(withdrawal_invoice)
    qr.save("reward_qr.png")
    print(f"QR Code saved as reward_qr.png")
    print(f"Lightning Invoice: {withdrawal_invoice}")

    # Wait for user action (close or restart)
    app.exec_()
