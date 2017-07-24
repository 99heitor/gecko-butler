#!/usr/bin/env python
from webapp2 import RequestHandler

import telegram
from setup import bot, setup, webhook
from bot_info import TOKEN, APP_URL
import json


class WebHookHandler(RequestHandler):
    def set_webhook(self):
        setup()
        s = bot.set_webhook(APP_URL + '/' + TOKEN)
        if s:
            self.response.write("Webhook setted")
        else:
            self.response.write("Webhook setup failed")

    def webhook_handler(self):
        # Retrieve the message in JSON and then transform it to Telegram object
        body = json.loads(self.request.body)
        update = telegram.Update.de_json(body, bot)
        webhook(update)