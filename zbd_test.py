from zbd import zbd
from variables import *
if __name__ == '__main__':

    z = zbd(ZEBEDEE_API_KEY,ZEBEDEE_CALLBACK_URL)
    # HERE Generating paywall so player has to pay.
    z.validate_lightning_address(ZEBEDEE_LIGHTNING_ADDRESS)
    print(z.get_wallet_details())
    
