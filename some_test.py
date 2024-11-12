import requests
import qrcode
from io import BytesIO
from PIL import Image
import time


class Config:
    API_KEY = "PA5peTC9rOUuU5kIN9t38CtiDMw38waw"  # Replace with your actual API key
    FEE = 0
    BITCOIN_VALUE = 1


class GameEngine:
    def __init__(self):
        self.totalSats = 0


class ZBDClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.zebedee.io"  # Correct base URL
        self.headers = {"Content-Type": "application/json", "apikey": self.api_key}

    def create_charge(self, amount, description=""):
        url = f"{self.base_url}/v0/charges"
        payload = {"amount": amount, "description": description}
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_charge(self, charge_id):
        url = f"{self.base_url}/v0/charges/{charge_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


class GameApp:
    def __init__(self):
        self.config = Config()
        self.game_engine = GameEngine()
        self.zbd_client = ZBDClient(self.config.API_KEY)
        self.charge_id = None

    def create_invoice(self):
        amount = int((self.config.BITCOIN_VALUE + self.config.FEE) * 1000)
        description = "Game Payment"
        try:
            charge = self.zbd_client.create_charge(amount, description)
            self.charge_id = charge["data"]["id"]
            self.create_invoice_qr_code(charge)
        except requests.exceptions.HTTPError as e:
            print("Failed to create invoice:", e)

    def create_invoice_qr_code(self, data):
        # Extract the Lightning invoice
        invoice_request = data["data"]["invoice"]["request"]

        # Generate QR code
        qr = qrcode.QRCode(
            version=20, error_correction=qrcode.constants.ERROR_CORRECT_L
        )
        qr.add_data(invoice_request)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Display the QR code (for the sake of this example, we save it to a file)
        img.save("qrcode.png")
        print("QR code generated and saved as 'qrcode.png'.")

        # In a GUI application, you would display the image in the interface
        # For now, we simulate the delay and call check_payment
        time.sleep(2)
        self.check_payment()

    def check_payment(self):
        if not self.charge_id:
            print("No charge ID found.")
            return
        try:
            charge_status = self.zbd_client.get_charge(self.charge_id)
            status = charge_status["data"]["status"]
            print(f"Charge status: {status}")
            if status == "completed":
                self.start_game()
            else:
                # Retry after 2 seconds
                print("Payment not completed yet. Checking again in 2 seconds...")
                time.sleep(2)
                self.check_payment()
        except requests.exceptions.HTTPError as e:
            print("Failed to check payment:", e)

    def start_game(self):
        self.game_engine.totalSats = 0
        print(f"Game started with {self.game_engine.totalSats} sats.")
        # Remove paywall or update the game state accordingly


# Instantiate and run the game app
if __name__ == "__main__":
    game_app = GameApp()
    game_app.create_invoice()
