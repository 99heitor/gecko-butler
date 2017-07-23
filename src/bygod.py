#!/usr/bin/env python2
# -*- coding: utf-8 -*-


def bygodify(bot, update, args):
    text = (' ').join(args)
    bot.send_message(chat_id=update.message.chat_id, text=bygod(text))


def bygod(query):
    sentences = query.split(",")
    bickering = ""
    for sentence in sentences[:-1]:
        if sentence.strip() != "":
            bickering += '"' + sentence.strip() + '"' + '... '
    if sentences[-1].strip() != "":
        bickering += '"' + sentences[-1].strip() + '" '

    final_message = u'Mas que chat desgraçado.\n\nQuando eu li ' + \
        bickering + u'já deu um desânimo. Perde toda a graça do negocio.'
    return final_message
