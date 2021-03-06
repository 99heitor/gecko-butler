# -*- coding: utf-8 -*-
import base64
import logging
import io
import requests
from google.cloud import vision
from google.cloud.vision import types

# Setting logger for this file
label_logger = logging.getLogger(__name__)
client = vision.ImageAnnotatorClient()


def command(bot, update):
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
        text = describe(bot.get_file(file_id))
    else:
        text = "Sorry, this is not a picture."
    bot.send_message(chat_id=message.chat_id,
                     reply_to_message_id=message.message_id, text=text,
                     parse_mode="Markdown")


def describe(photo):
    url = photo.file_path
    image_bytes = io.BytesIO(requests.get(url).content)
    results = get_labels(image_bytes)
    log = ""
    response = "I see...\n"
    for result in results:
        response += "*{}* : {:.1%}\n".format(
            result.description,
            result.score
        )
        log += "[{}: {}] ".format(result.description, result.score)
    label_logger.info(log)
    return response


def get_labels(image):
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return labels
