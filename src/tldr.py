# -*- coding: utf-8 -*-
import requests
from bot_info import SMMRY_KEY
from re import sub, findall


def tldr_command(bot, update, args):
    message = update.message
    if len(args) >= 1 and len(get_urls(args[0])) > 0:
        payload = [('SM_API_KEY', SMMRY_KEY)]

        if len(args) == 2 and args[1].isdigit():
            payload.append(('SM_LENGTH', args[1]))
        else:
            payload.append(('SM_LENGTH', 5))

        payload.append(('SM_KEYWORD_COUNT', 5))
        payload.append(('SM_URL', args[0]))
        reply_to = message.message_id

        if len(get_urls(args[0])) == 0:
            text = "Use /tldr <URL> or /tldr as reply to a message that contains a URL"
        else:
            text = tldr(payload)
    else:
        if (not message.reply_to_message or
            not message.reply_to_message.text or
                len(get_urls(message.reply_to_message.text)) == 0):

            text = "Use /tldr <URL> or /tldr as reply to a message that contains a URL"

            reply_to = message.message_id
        else:
            text = ""
            url = get_urls(message.reply_to_message.text)
            reply_to = message.reply_to_message.message_id
            if message.from_user.username:
                text = "@{} is too lazy to read.\n\n".format(
                    message.from_user.username)

            payload = [('SM_API_KEY', SMMRY_KEY)]
            if len(args) >= 1 and args[0].isdigit():
                payload.append(('SM_LENGTH', args[0]))
            else:
                payload.append(('SM_LENGTH', 5))
            payload.append(('SM_KEYWORD_COUNT', 5))
            payload.append(('SM_URL', url))
            text += tldr(payload)

    bot.send_message(chat_id=message.chat_id,
                     reply_to_message_id=reply_to,
                     text=text,
                     parse_mode="Markdown")


def tldr(payload):
    response = requests.get(
        'http://api.smmry.com/&SM_WITH_BREAK', params=payload).json()

    title = ""
    print response
    if 'sm_api_error' not in response:
        if 'sm_api_title' in response:
            title = u'*{}*\n\n'.format(response['sm_api_title'].replace(
                "\\", "").replace("&#2013265929;", u"é"))

        top_keywords = ""
        _, url = payload[-1]
        if ".br" not in url[0] and 'sm_api_keyword_array' in response:
            top_keywords = "\n\n`Top keywords: {}`".format(
                ' '.join(response['sm_api_keyword_array']))

        if 'sm_api_content' in response:
            sentences = sub(r'\[BREAK\]\s?', '\n',
                            response['sm_api_content']).strip()
            text = u"{0}{1}{2}".format(
                title, sentences, top_keywords)
        else:
            text = "Too bad, I can't summarize that."
    elif response['sm_api_error'] == 3 and response['sm_api_message'] == 'TEXT IS TOO SHORT':
        text = "But why? The text is already too short."
    elif response['sm_api_error'] == 2:
        text = "That's enough TLDR for today, try again tomorrow."
    else:
        text = "I can't summarize that, for some unkown reason."

    return text


def get_urls(text):
    return findall(r'(https?://[^\s]+)', text)
