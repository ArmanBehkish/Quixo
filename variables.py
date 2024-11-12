# Store constants for the application
import os

# ZEBEDEE API Configurations
ZEBEDEE_API_KEY = os.getenv("ZEBEDEE_API_KEY", "Ywn2gREd7ysTeNKdntS12NLjyvvkRh3F")
ZEBEDEE_API_URL = "https://api.zebedee.io/v1"
ZEBEDEE_CALLBACK_URL = "http://127.0.0.1:5000"
ZEBEDEE_LIGHTNING_ADDRESS = "koraty@zbd.gg"
# Paywall and Reward Configuration
INVOICE_EXPIRY = 600  # Expiry time in seconds for invoices
REWARD_AMOUNT = 10000  # Default reward amount in millisats
PAYWALL_AMOUNT = 1000

# Other application constants
PLAYER_REWARD_DESCRIPTION_TEMPLATE = "Congratulations Player {winner_id}! You've won the game."