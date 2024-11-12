# Store constants for the application
import os

# ZEBEDEE API Configurations
ZEBEDEE_API_KEY = os.getenv("ZEBEDEE_API_KEY", "JY2knFEHU13TxAPqqSH240nx7aao4OrN")
ZEBEDEE_API_URL = "https://api.zebedee.io/v1"

# Paywall and Reward Configuration
INVOICE_EXPIRY = 600  # Expiry time in seconds for invoices
REWARD_AMOUNT = 1000  # Default reward amount in millisats


# Other application constants
PLAYER_REWARD_DESCRIPTION_TEMPLATE = "Congratulations Player {winner_id}! You've won the game."