from typing import List

from telegram import Update
from telegram.ext import (
    Updater,
    Filters,
    CallbackContext,
    MessageHandler,
)

from coinbase import CoinbaseTicker
from rates import CurrencyPair

DEFAULT_DISPLAY_CURRENCY = "USD"
MESSAGE_RATE_PATTERN = r"(?i)[a-zA-Z]+[\/](?i)[a-zA-Z]*"
MESSAGE_RATE_DISPLAY_FORMAT = "1 {} is {} {}"


def send_rates(update: Update, context: CallbackContext):
    pair = CurrencyPair.from_str(value=update.message.text, fallback_counter=DEFAULT_DISPLAY_CURRENCY)

    rate, errors = CoinbaseTicker(pair).query()

    if errors is not None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(errors))
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MESSAGE_RATE_DISPLAY_FORMAT.format(
                rate.pair.base,
                rate.amount_formatted(),
                rate.pair.counter
            )
        )


class CryptoRatesBot:

    def __init__(self, bot_token: str, allowed_updates: List[str]):
        self._allowed_updates = allowed_updates
        self._updater = Updater(token=bot_token, use_context=True)
        self._dispatcher = self._updater.dispatcher
        self.register_handlers()

    def process_update(self, update):
        self._dispatcher.process_update(Update.de_json(update, self._updater.bot))

    def register_handlers(self):
        self._dispatcher.add_handler(MessageHandler(Filters.regex(MESSAGE_RATE_PATTERN), send_rates))
