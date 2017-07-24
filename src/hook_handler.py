#!/usr/bin/env python
from webapp2 import RequestHandler

import telegram
from telegram import bot
from gecko_butler import bot, setup, webhook
from application import TOKEN
import json

APP_URL = "http://geckobutler.appspot.com"


class WebHookHandler(RequestHandler):
    def set_webhook(self):
        '''
        Set webhook for your bot
        '''
        setup()
        s = bot.setWebhook(APP_URL + '/' + TOKEN)
        if s:
            self.response.write("Webhook setted")
        else:
            self.response.write("Webhook setup failed")

    def webhook_handler(self):
        # Retrieve the message in JSON and then transform it to Telegram object
        body = json.loads(self.request.body)
        update = telegram.Update.de_json(body)
        webhook(update)