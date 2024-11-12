import requests
import qrcode
from variables import ZEBEDEE_API_KEY, ZEBEDEE_API_URL, INVOICE_EXPIRY

class PaywallManager:
    def __init__(self):
        self.api_key = ZEBEDEE_API_KEY
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def create_invoice(self, amount):
        url = f"{ZEBEDEE_API_URL}/v1/charges"
        print(f"Creating invoice at URL: {url}")
        data = {
            "amount": amount,
            "expiry": INVOICE_EXPIRY,
            "description": "Access the game!"
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            invoice = response.json()
            self._generate_qr_code(invoice["invoice"]["request"])
            return invoice["id"]
        else:
            print(f"Error creating invoice: {response.status_code} - {response.json()}")
            return None

    def _generate_qr_code(self, payment_request):
        img = qrcode.make(payment_request)
        img.save("paywall_qrcode.png")
        print("QR Code generated and saved as 'paywall_qrcode.png'.")

    def check_payment(self, invoice_id):
        url = f"{ZEBEDEE_API_URL}/v1/charges/{invoice_id}"
        print(f"Checking payment status at URL: {url}")
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            status = response.json().get("status")
            if status == "completed":
                print("Payment confirmed. Removing paywall.")
                return True
            elif status == "pending":
                print("Payment pending. Checking again shortly.")
                return False
        else:
            print(f"Error checking payment status: {response.status_code} - {response.json()}")
            return False
