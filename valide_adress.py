import requests
from variables import ZEBEDEE_API_KEY

# Replace with your actual API key and the address you want to validate
api_key = ZEBEDEE_API_KEY
address = "koraty@zbd.gg"

url = f"https://api.zebedee.io/v0/ln-address/validate/{address}"

headers = {"apikey": api_key}

response = requests.request("GET", url, headers=headers)

print(response.text)
