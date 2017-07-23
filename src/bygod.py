# -*- coding: utf-8 -*-
def bygodify(bot, update, args):
    text = (' ').join(args)
    bot.send_message(chat_id=update.message.chat_id, text=bygod(text))

def bygod(query):
    values = query.split(",")
    bickering = "" 
    for v in values[:-1]:
        if v.strip() != "":
            bickering += '"' + v.strip() + '"' + '... '
    if values[-1].strip() != "":
        bickering += '"' + values[-1].strip() + '" '
    
    final_message = u'Mas que chat desgraçado.\n\nQuando eu li ' + bickering + u'já deu um desânimo. Perde toda a graça do negocio.'
    return final_message