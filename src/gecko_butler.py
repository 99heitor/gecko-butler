#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import json
import logging
from bygod import bygod, bygodify
from labels import describe
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (CommandHandler, Filters, InlineQueryHandler,
                          MessageHandler, Updater)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello world!")


def gecko_inline(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()

    results.append(InlineQueryResultArticle(
        id="Bygode",
        title="Bygodify",
        input_message_content=InputTextMessageContent(bygod(query))
    ))
    bot.answer_inline_query(update.inline_query.id, results)


def main():
    with open('keys/bot_token.json') as json_data:
        data = json.load(json_data)
        updater = Updater(token=data['token'])

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    describe_handler = CommandHandler('describe', describe)
    bygod_handler = CommandHandler('bygodify', bygodify, pass_args=True)

    inline_handler = InlineQueryHandler(gecko_inline)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(describe_handler)
    dispatcher.add_handler(inline_handler)
    dispatcher.add_handler(bygod_handler)
    dispatcher.add_error_handler(error)

    updater.start_polling(bootstrap_retries=3)
    updater.idle()


if __name__ == "__main__":
    main()
