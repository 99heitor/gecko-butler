#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import base64
import os
import urllib
import logging
from time import sleep

from googleapiclient.discovery import build
from telegram.error import (TelegramError)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "keys/vision_key.json"

label_logger = logging.getLogger(__name__)


def describe(bot, update):
    message = update.message
    if message.chat.username:
        label_logger.info(
            "Request from user: " + message.chat.username)
    elif message.chat.title:
        label_logger.info(
            "Request from chat: " + message.chat.title)

    if not message.reply_to_message:
        text = "Use the command /describe as a reply to a picture."
    elif message.reply_to_message.photo:
        file_id = message.reply_to_message.photo[-1].file_id
        text = pretty_labels(bot.get_file(file_id), file_id)
    else:
        text = "Sorry, this is not a picture."
    bot.send_message(chat_id=message.chat_id,
                     reply_to_message_id=message.message_id, text=text,
                     parse_mode="Markdown")


def get_labels(photo_file):
    service = build('vision', 'v1', cache_discovery=False)

    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 10
                }]
            }]
        })

    response = service_request.execute()
    return response['responses'][0]['labelAnnotations']


def pretty_labels(photo, name):
    url = photo.file_path
    save_path = "../photos/" + str(name) + ".jpg"
    urllib.urlretrieve(url, save_path)
    results = get_labels(save_path)
    log = ""
    response = "I see...\n"
    for result in results:
        response += "*" + result['description'] + \
            "* : " + '{:.1%}'.format(result['score']) + '\n'
        log += '[' + result['description'] + ': ' + str(result['score']) + '] '
    label_logger.info(log)
    return response
