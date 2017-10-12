#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import json
import logging

import telegram
from telegram.ext import (CommandHandler, Dispatcher, InlineQueryHandler)
from webapp2 import RequestHandler

from queries import bygodify, describe, tldr
from bot_info import TOKEN, APP_URL
from bot import app

# Setting log structure
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def get_bot():
    if app.registry.get('bot') is None:
        app.registry['bot'] = telegram.Bot(TOKEN)
    return app.registry['bot']


def get_dispatcher():
    if app.registry.get('dispatcher') is None:
        app.registry['dispatcher'] = setup(get_bot())
    return app.registry['dispatcher']


class WebHookHandler(RequestHandler):

    def set_webhook(self):
        if get_bot().set_webhook(APP_URL + '/' + TOKEN):
            self.response.write("Webhook setted")
        else:
            self.response.write("Webhook setup failed")

    def webhook_handler(self):
        # Retrieve the message in JSON and then transform it to Telegram object
        body = json.loads(self.request.body)
        update = telegram.Update.de_json(body, get_bot())
        get_dispatcher().process_update(update)


def setup(bot):
    dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)
    start_handler = CommandHandler('start', start)
    describe_handler = CommandHandler('describe', describe.command)
    tldr_handler = CommandHandler('tldr', tldr.command,
                                  pass_args=True)
    bygod_handler = CommandHandler('bygodify', bygodify.command,
                                   pass_args=True)
    inline_handler = InlineQueryHandler(bygodify.inline)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(describe_handler)
    dispatcher.add_handler(tldr_handler)
    dispatcher.add_handler(inline_handler)
    dispatcher.add_handler(bygod_handler)
    dispatcher.add_error_handler(error)
    return dispatcher


def error(bot, update, error):
    logger = logging.getLogger(__name__)
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Hello. Reply a picture with the command /describe, "
                     "and I will tell you what I see.")
