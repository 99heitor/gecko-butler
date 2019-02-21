from threading import Thread
from telegram import Bot
from queue import Queue
from telegram.ext import (CommandHandler, Dispatcher, InlineQueryHandler)
from queries import bygodify, describe, tldr
import logging

def error(bot, update, error):
    logger = logging.getLogger(__name__)
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Hello. Reply a picture with the command /describe, "
                     "and I will tell you what I see.")
def setup(token):
    bot = Bot(token)
    update_queue = Queue()
    
    dispatcher = Dispatcher(bot, update_queue)
    
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
    
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()
    return (update_queue, dispatcher)
