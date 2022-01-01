import http
import logging
import os

from flask import Flask, request
from telegram import Update
from werkzeug.wrappers import Response

from bot import CryptoRatesBot

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

app = Flask(__name__)
bot = CryptoRatesBot(bot_token=os.environ["BOT_TOKEN"], allowed_updates=[Update.MESSAGE])


@app.post("/")
def index():
    bot.process_update(request.get_json(force=True))
    return Response("", http.HTTPStatus.NO_CONTENT)
