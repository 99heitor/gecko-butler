import requests
from bot_info import SMMRY_KEY


def tldr_command(bot, update, args):
    payload = [('SM_API_KEY', SMMRY_KEY)]
    payload.append(('SM_LENGTH', args[1]))
    payload.append(('SM_URL', args[0]))
    bot.send_message(chat_id=update.message.chat_id, text=tldr(payload))


def tldr(payload):
    response = requests.get(
        'http://api.smmry.com/&SM_WITH_BREAK', params=payload).json()
    return response['sm_api_content'].replace("[BREAK]", '\n')
