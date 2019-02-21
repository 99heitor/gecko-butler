# !/usr/bin/env python3
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "vision_key.json"
import sys
import json
import logging

from telegram import Update
from bot_info import TOKEN, APP_URL
from flask import Flask, request
from bot_setup import setup

app = Flask(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

update_queue, dispatcher = setup(TOKEN)

@app.route('/set_webhook')
def set_webhook():
    if dispatcher.bot.set_webhook(APP_URL + '/' + TOKEN):
        return "Webhook set"
    else:
        return "Webhook setup failed"

@app.route("/{}".format(TOKEN), methods=["POST"])
def webhook_handler():
    # Retrieve the message in JSON and then transform it to Telegram object
    update = Update.de_json(request.get_json(), dispatcher.bot)
    update_queue.put(update)
    return "ok!", 200


if __name__ == "__main__":
    # Execute app on localhost instead of app engine.
    # Be sure to update APP_URL on bot_info.py (not tracked)
    app.run(host='127.0.0.1', port=8080, debug=True)
