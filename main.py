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


from variables import *
from zbd import zbd
import qrcode
import time
# Main function
if __name__ == '__main__':
    zbd_client = zbd(apikey=ZEBEDEE_API_KEY)

    # Generate paywall
    charge_response = zbd_client.create_charge(
        amount_of_seconds_to_expire_after=INVOICE_EXPIRY,
        amount_msats=PAYWALL_AMOUNT,  # Example amount >=1000 and /1000
        description="Pay to start the game"
    )
    charge_id = charge_response['id']
    charge_details = zbd_client.get_charge_details(charge_id)
    lightning_invoice = charge_details['invoice']['request']

    print("Please pay the following invoice to start the game:")
    qr = qrcode.make(lightning_invoice)
    qr.save("paywall_qr.png")
    print(f"QR Code saved as paywall_qr.png")
    print(f"Lightning Invoice: {lightning_invoice}")

    # Wait for payment confirmation (simplified for demonstration)
    #HACK To avoid payment
    input("Press Enter after payment...")

    # Poll for payment confirmation
    # while True:
    #     payment_status = zbd_client.check_payment_status(charge_id)
    #     if payment_status == 'completed':
    #         print("Payment confirmed. Starting the game...")
    #         break
    #     elif payment_status == 'failed':
    #         print("Payment failed. Exiting...")
    #         exit(1)
    #     else:
    #         print("Waiting for payment confirmation...")
    #         time.sleep(5)  # Wait for 5 seconds before checking again

    # Start the game
    g = Game()
    g.print()
    player1 = MyPlayer()
    player2 = RandomPlayer()
    winner = g.play(player1, player2)
    g.print()
    print(f"Winner: Player {winner}")

    # Generate withdrawal request for the winner
    reward_description = PLAYER_REWARD_DESCRIPTION_TEMPLATE.format(winner_id=winner)
    withdrawal_response = zbd_client.create_withdrawal_request(
        amount_of_seconds_to_expire_after=INVOICE_EXPIRY,
        amount_msats=REWARD_AMOUNT,
        description="Got your reward",
        internal_id="11af01d092444a317cb33faa6b8304b8"
    )

    withdrawal_id = withdrawal_response['id']
    withdrawal_details = zbd_client.get_withdrawal_request_details(withdrawal_id)
    withdrawal_invoice = withdrawal_details['invoice']['request']

    print("Congratulations! Here is your reward:")
    qr = qrcode.make(withdrawal_invoice)
    qr.save("reward_qr.png")
    print(f"QR Code saved as reward_qr.png")
    print(f"Lightning Invoice: {withdrawal_invoice}")
    
