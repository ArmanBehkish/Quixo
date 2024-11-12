"""_summary_

Ensure to have a lightning adress.
But the best thing is that your ZBD username is the same as your Lightning Address! 
In other words, when you create a username, you’ll automatically get a Lightning Address for the same name. 
For example, if you choose “NatoshiSakamoto” as your username, you’ll get a Lightning Address natoshisakamoto@zbd.gg 
(and a https://zbd.gg/natoshisakamoto profile page).
TO DO on playstore app, not on the dashboard.
"""
import requests
import uuid

# Replace with your actual API key and URL
ZEBEDEE_API_KEY = "JY2knFEHU13TxAPqqSH240nx7aao4OrN"
ZEBEDEE_API_URL = "https://api.zebedee.io/v0"

def generate_internal_id():
    return str(uuid.uuid4())

def create_invoice(amount, description, internal_id):
    url = f"{ZEBEDEE_API_URL}/payments"
    headers = {
        "Content-Type": "application/json",
        "apikey": ZEBEDEE_API_KEY
    }
    data = {
        "amount": amount,
        "description": description,
        "internalId": internal_id
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        invoice = response.json().get("invoice")
        return invoice
    else:
        print(f"Error creating invoice: {response.status_code} - {response.json()}")
        return None

# Example usage
amount = 1000  # Amount in millisats
description = "My Payment Description"
internal_id = "5289f02c-41c4-4022-85db-b26664bb6f06"
invoice = create_invoice(amount, description, internal_id)
print(f"Generated Invoice: {invoice}")
print(f"Generated Internal ID: {internal_id}")
