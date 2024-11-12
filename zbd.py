import requests, json, math

class zbd:

    def __init__(self, apikey, callback_url=""):
        self.apikey = apikey
        self.callback_url = callback_url

    def handle_request(self, method, url, headers, payload=None):
        response = method(url, headers=headers, data=payload)

        try:
            response_json = response.json()

            if response.status_code != 200:
                raise ValueError(f"Request failed with status code: {response.status_code}")

            return response_json["data"]
        except Exception as e:
            raise RuntimeError(f"An error occurred: {e}, Response: {response.message}")

    def get_wallet_details(self):
        URL = 'https://api.zebedee.io/v0/wallet'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}
        return self.handle_request(requests.get, URL, heads)

    def create_charge(self, amount_of_seconds_to_expire_after, amount_msats, description, internal_id=None):
        URL = 'https://api.zebedee.io/v0/charges'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}

        payload = json.dumps({
            "expiresIn": amount_of_seconds_to_expire_after,
            "amount": str(amount_msats),
            "description": description,
            "internalId": internal_id,
            "callbackUrl": self.callback_url
        })
        return self.handle_request(requests.post, URL, heads, payload)

    def get_charge_details(self, zbd_id):
        URL = f'https://api.zebedee.io/v0/charges/{zbd_id}'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}
        return self.handle_request(requests.get, URL, heads)

    def create_static_charge(self, min_amount_msats, max_amount_msats, description, success_message=None, internal_id=None, allowed_slots=None):
        URL = 'https://api.zebedee.io/v0/static-charges'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}

        payload = json.dumps({
            "allowedSlots": allowed_slots,
            "minAmount": str(min_amount_msats),
            "maxAmount": str(max_amount_msats),
            "description": description,
            "internalId": internal_id,
            "callbackUrl": self.callback_url,
            "successMessage": success_message
        })
        return self.handle_request(requests.post, URL, heads, payload)

    def update_static_charge_details(self, id, min_amount_msats, max_amount_msats, description, success_message=None, allowed_slots=None):
        url = f"https://api.zebedee.io/v0/static-charges/{id}"
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}
        payload = {
            "allowedSlots": allowed_slots,
            "minAmount": str(min_amount_msats),
            "maxAmount": str(max_amount_msats),
            "description": description,
            "callbackUrl": self.callback_url,
            "successMessage": success_message
        }
        return self.handle_request(requests.patch, url, heads, json.dumps(payload))

    def get_static_charge_details(self, zbd_id):
        URL = f'https://api.zebedee.io/v0/static-charges/{zbd_id}'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}
        return self.handle_request(requests.get, URL, heads)

    def create_withdrawal_request(self, amount_of_seconds_to_expire_after, amount_msats, description, internal_id=None):
        URL = 'https://api.zebedee.io/v0/withdrawal-requests'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}

        payload = json.dumps({
            "expiresIn": amount_of_seconds_to_expire_after,
            "amount": str(amount_msats),
            "description": description,
            "internalId": internal_id,
            "callbackUrl": self.callback_url
        })
        return self.handle_request(requests.post, URL, heads, payload)

    def get_withdrawal_request_details(self, zbd_id):
        URL = f'https://api.zebedee.io/v0/withdrawal-requests/{zbd_id}'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}
        return self.handle_request(requests.get, URL, heads)

    def send_keysend_payment(self, public_key, amount_msats, metadata=None, tlv_records=None):
        URL = 'https://api.zebedee.io/v0/keysend-payment'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}

        payload = json.dumps({
            "amount": str(amount_msats),
            "pubkey": str(public_key),
            "tlvRecords": tlv_records,
            "metadata": metadata,
            "callbackUrl": f"{self.callback_url}"
        })
        return self.handle_request(requests.post, URL, heads, payload)

    def pay_invoice(self, invoice, description, internal_id=None, amount=None):
        URL = 'https://api.zebedee.io/v0/payments'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}

        if amount:
            payload = json.dumps({
                "description": description,
                "internalId": internal_id,
                "invoice": invoice,
                "callbackUrl": self.callback_url,
                "amount": str(amount)
            })
        else:
            payload = json.dumps({
                "description": description,
                "internalId": internal_id,
                "invoice": invoice,
                "callbackUrl": self.callback_url
            })
        return self.handle_request(requests.post, URL, heads, payload)

    def get_payment_details(self, zbd_id):
        URL = f'https://api.zebedee.io/v0/payments/{zbd_id}'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}
        return self.handle_request(requests.get, URL, heads)

    def validate_lightning_address(self, lightning_address):
        URL = f'https://api.zebedee.io/v0/ln-address/validate/{lightning_address}'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}
        return self.handle_request(requests.get, URL, heads)

    def send_payment_to_lightning_address(self, lightning_address, amount_msats, comment, internal_id=None):
        URL = 'https://api.zebedee.io/v0/ln-address/send-payment'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}

        payload = json.dumps({
            "lnAddress": lightning_address,
            "amount": str(amount_msats),
            "unit": "msats",
            "comment": comment,
            "callbackUrl": self.callback_url,
            "internalId": internal_id
        })
        return self.handle_request(requests.post, URL, heads, payload)

    def fetch_charge_from_lightning_address(self, lightning_address, amount_msats, description):
        URL = 'https://api.zebedee.io/v0/ln-address/fetch-charge'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}

        payload = json.dumps({
            "lnaddress": lightning_address,
            "amount": str(amount_msats),
            "description": description
        })

        return self.handle_request(requests.post, URL, heads, payload)

    def send_payment_to_gamertag(self, gamertag, amount_msats, description):
        URL = 'https://api.zebedee.io/v0/gamertag/send-payment'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}

        payload = json.dumps({
            "gamertag": gamertag,
            "amount": str(amount_msats),
            "description": description
        })
        return self.handle_request(requests.post, URL, heads, payload)

    def get_gamertag_transaction_details(self, zbd_id):
        URL = f'https://api.zebedee.io/v0/gamertag/transaction/{zbd_id}'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}
        return self.handle_request(requests.get, URL, heads)

    def get_user_id_from_gamertag(self, gamertag):
        URL = f'https://api.zebedee.io/v0/user-id/gamertag/{gamertag}'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}
        return self.handle_request(requests.get, URL, heads)["id"]

    def get_gamertag_from_user_id(self, user_id):
        URL = f'https://api.zebedee.io/v0/gamertag/user-id/{user_id}'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}
        return self.handle_request(requests.get, URL, heads)["gamertag"]

    def fetch_charge_from_gamertag(self, gamertag, amount_msats, description, internal_id=None):
        URL = 'https://api.zebedee.io/v0/gamertag/charges'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}

        payload = json.dumps({
            "amount": str(amount_msats),
            "gamertag": gamertag,
            "description": description,
            "callbackUrl": self.callback_url,
            "internalId": internal_id
        })
        return self.handle_request(requests.post, URL, heads, payload)

    def is_supported_region(self, ip):
        URL = f'https://api.zebedee.io/v0/is-supported-region/{ip}'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}
        return self.handle_request(requests.get, URL, heads)

    def get_zbd_prod_server_ip(self):
        URL = f'https://api.zebedee.io/v0/prod-ips'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}
        return self.handle_request(requests.get, URL, heads)

    def get_btc_usd_quote_price(self):
        URL = 'https://api.zebedee.io/v0/btcusd'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}
        return self.handle_request(requests.get, URL, heads)["btcUsdPrice"]

    def convert_usd_to_sats(self, usd_amount):
        btc_price = self.get_btc_usd_quote_price()
        sats_amount = math.floor(round(int(usd_amount) / int(btc_price), 8) * 100000000)
        return sats_amount

    def convert_msats_to_sats(self, amount_msats):
        return str(math.floor(int(amount_msats) / 1000))

    def convert_sats_to_msats(self, amount_sats):
        return str(amount_sats) + "000"

    def transfer_zbd_funds(self, amount_msats, receiver_wallet_id):
        URL = 'https://api.zebedee.io/v0/internal-transfer'
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}

        payload = json.dumps({
            "amount": str(amount_msats),
            "receiverWalletId": receiver_wallet_id
        })
        return self.handle_request(requests.post, URL, heads, payload)

    def get_static_charge_metadata(self, id):
        url = f"https://api.zebedee.io/v0/request-static-charges/{id}"
        heads = {'Content-Type': 'application/json', 'apikey': self.apikey}
        return self.handle_request(requests.get, url, heads)
    
    def check_payment_status(self, charge_id):
        charge_details = self.get_charge_details(charge_id)
        return charge_details['status']

