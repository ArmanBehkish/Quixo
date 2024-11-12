import requests
import qrcode
from variables import ZEBEDEE_API_KEY, ZEBEDEE_API_URL, REWARD_AMOUNT

class RewardManager:
    def __init__(self):
        self.api_key = ZEBEDEE_API_KEY
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def create_withdrawal(self, amount):
        url = f"{ZEBEDEE_API_URL}/v1/withdrawal-requests"
        print(f"Creating withdrawal request at URL: {url}")
        data = {
            "amount": amount,
            "description": "Withdraw your rewards!"
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            withdrawal = response.json()
            self._generate_qr_code(withdrawal["invoice"]["request"])
            return withdrawal["id"]
        else:
            print(f"Error creating withdrawal request: {response.status_code} - {response.json()}")
            return None

    def _generate_qr_code(self, payment_request):
        img = qrcode.make(payment_request)
        img.save("withdrawal_qrcode.png")
        print("QR Code generated and saved as 'withdrawal_qrcode.png'.")

    def check_withdrawal_status(self, withdrawal_id):
        url = f"{ZEBEDEE_API_URL}/v1/withdrawal-requests/{withdrawal_id}"
        print(f"Checking withdrawal status at URL: {url}")
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            status = response.json().get("status")
            if status == "completed":
                print("Withdrawal completed. Resetting reward balance.")
                return True
            elif status == "pending":
                print("Withdrawal pending. Checking again shortly.")
                return False
        else:
            print(f"Error checking withdrawal status: {response.status_code} - {response.json()}")
            return False
