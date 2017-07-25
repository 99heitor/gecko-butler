#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import logging
from bygodify import bygodify_command, bygodify
from describe import describe_command
from tldr import tldr_command
from bot_info import TOKEN
from telegram import InlineQueryResultArticle, InputTextMessageContent, Bot
from telegram.ext import (CommandHandler, Filters, InlineQueryHandler,
                          MessageHandler, Dispatcher)

# Setting log structure
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

bot = Bot(TOKEN)

dispatcher = None


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Hello. Reply a picture with the command /describe, "
                     "and I will tell you what I see.")


def gecko_inline(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()

    results.append(InlineQueryResultArticle(
        id="Bygode",
        title="Bygodify",
        input_message_content=InputTextMessageContent(bygodify(query))
    ))
    bot.answer_inline_query(update.inline_query.id, results)


def setup():
    global dispatcher
    dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)

    start_handler = CommandHandler('start', start)
    describe_handler = CommandHandler('describe', describe_command)
    tldr_handler = CommandHandler('tldr', tldr_command,
                                  pass_args=True)
    bygod_handler = CommandHandler('bygodify', bygodify_command,
                                   pass_args=True)
    inline_handler = InlineQueryHandler(gecko_inline)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(describe_handler)
    dispatcher.add_handler(tldr_handler)
    dispatcher.add_handler(inline_handler)
    dispatcher.add_handler(bygod_handler)
    dispatcher.add_error_handler(error)
    return dispatcher


def webhook(update):
    global dispatcher
    # Manually get updates and pass to dispatcher
    dispatcher.process_update(update)
