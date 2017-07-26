# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
from re import findall, sub

import requests

from bot_info import SMMRY_KEY


def tldr_command(bot, update, args):
    message = update.message
    payload = []
    text = ""
    default_length = 5

    # Treat the message as a standalone message.
    if args and get_urls(args[0]):

        # Is there a 'sentence count' argument?
        if len(args) == 2 and args[1].isdigit():
            payload.append(('SM_LENGTH', args[1]))
        else:
            payload.append(('SM_LENGTH', default_length))

        payload.append(('SM_URL', args[0]))
        reply_to = message.message_id
        text = tldr(payload)

    # Treat the message as a reply
    else:
        # Is it really a reply to a link?
        if (not message.reply_to_message or
                not message.reply_to_message.text or
                not get_urls(message.reply_to_message.text)):

            text = ("Use /tldr <URL> or /tldr as reply "
                    "to a message that contains a URL")
            reply_to = message.message_id
        # Yes, it is.
        else:
            url = get_urls(message.reply_to_message.text)[0]
            if message.from_user.username:
                text = "@{} is too lazy to read.\n\n".format(
                    message.from_user.username)

            # Is there a 'sentence count' argument?
            if len(args) >= 1 and args[0].isdigit():
                payload.append(('SM_LENGTH', args[0]))
            else:
                payload.append(('SM_LENGTH', default_length))

            payload.append(('SM_URL', url))
            reply_to = message.reply_to_message.message_id
            text += tldr(payload)

    bot.send_message(chat_id=message.chat_id,
                     reply_to_message_id=reply_to,
                     text=text,
                     parse_mode='Markdown')


def tldr(payload):

    top_keywords = ""
    title = ""
    _, url = payload[-1]
    omit_keywords_for = ['.br', '/pt-br/']

    response = requests.get(
        "http://api.smmry.com/SM_API_KEY={}"
        "&SM_WITH_BREAK&SM_KEYWORD_COUNT=5".format(SMMRY_KEY),
        params=payload).json()

    if 'sm_api_error' not in response:
        if 'sm_api_title' in response:
            title = u'*{}*\n\n'.format(decode_trash(response['sm_api_title']))

        if not any(x in url for x in omit_keywords_for):
            top_keywords = "\n\n`Top keywords: `"
            for word in response['sm_api_keyword_array']:
                top_keywords += u"`{} `".format(decode_trash(word))

        sentences = sub(r'\[BREAK\]\s?', '\n',
                        response['sm_api_content']).strip()

        text = u"{0}{1}{2}".format(title, sentences, top_keywords)

    # Text too short
    elif (response['sm_api_error'] == 3 and
          response['sm_api_message'] == 'TEXT IS TOO SHORT'):
        text = "But why? The text is already too short."
    # API limit
    elif response['sm_api_error'] == 2:
        text = "That's enough TLDR for today, try again tomorrow."
    # Another error
    else:
        text = "I can't summarize that, for some unkown reason."

    return text


def get_urls(text):
    return findall(r'(https?://[^\s]+)', text)


def decode_trash(text):
    hparse = HTMLParser()
    return hparse.unescape(
        text.replace('\\', '').replace('&#2013265929;', u'é'))
