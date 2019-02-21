# -*- coding: utf-8 -*-
from telegram import InlineQueryResultArticle, InputTextMessageContent


def command(bot, update, args):
    text = (' ').join(args)
    bot.send_message(chat_id=update.message.chat_id, text=bygodify(text))


def inline(bot, update):
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


def bygodify(query):
    sentences = query.split(",")
    bickering = ""
    for sentence in sentences[:-1]:
        if sentence.strip() != "":
            bickering += '"' + sentence.strip() + '"' + '... '
    if sentences[-1].strip() != "":
        bickering += '"' + sentences[-1].strip() + '" '

    final_message = 'Mas que chat desgraçado.\n\nQuando eu li ' + \
        bickering + 'já deu um desânimo. Perde toda a graça do negocio.'
    return final_message
