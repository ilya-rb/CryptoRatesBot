import logging

from telegram import Update

from bot import CryptoRatesBot
from config import BOT_TOKEN

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

bot = CryptoRatesBot(bot_token=BOT_TOKEN, allowed_updates=[Update.MESSAGE])
bot.start()
