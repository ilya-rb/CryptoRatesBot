import requests

from rates import Ticker, Rate, CurrencyPair

RATES_BASE_URL = "https://api.coinbase.com/v2/exchange-rates"

# Example: https://api.coinbase.com/v2/exchange-rates?currency=BTC
PARAM_CURRENCY = "currency"

# Examples:
# 200: {
#   "data": {
#     "currency": "BTC",
#     "rates": {
#       "AED": "36.73",
#       "AFN": "589.50",
#       ...
#     }
#   }
# }
# 400: {
# "errors": [
#   {
#     "id": "invalid_request",
#     "message": "Currency is invalid"
#   }
#  ]
# }

KEY_DATA = "data"
KEY_CURRENCY = "currency"
KEY_RATES = "rates"
KEY_ERRORS = "errors"
KEY_MESSAGE = "message"


class CoinbaseTicker(Ticker):

    def __init__(self, pair: CurrencyPair):
        super().__init__(pair)

    def query(self):
        payload = {PARAM_CURRENCY: self.pair.base}
        response = requests.get(url=RATES_BASE_URL, params=payload).json()

        print(f"HTTP call :: {RATES_BASE_URL} PAYLOAD :: {payload}")
        print(f"RESPONSE :: {response}")

        if KEY_ERRORS in response:
            errors = map(lambda error: error[KEY_MESSAGE], response[KEY_ERRORS])
            return None, errors
        else:
            data = response[KEY_DATA]
            return Rate(pair=self.pair, amount=float(data[KEY_RATES][self.pair.counter])), None
