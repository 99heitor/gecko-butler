import base64
from apiclient.discovery import build
import urllib
import io
import os
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "keys/vision_key.json"

def describe(bot,update):
    print("Request from chat:"+ str(update.message.chat_id))
    attempts = 0;
    if not update.message.reply_to_message:
        text="Use the command /describe as a reply to a picture."
    elif update.message.reply_to_message.photo:
        while attempts < 3:
            try:
                id = update.message.reply_to_message.photo[-1].file_id
                text=pretty_labels(bot.get_file(id),id)
                attempts = 3
            except TelegramError as error:
                print ("TelegramError was raised. Trying again...")
                attempts += 1
                sleep(1)
    else:
        text="Sorry, this is not a picture."
    bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id,text=text,parse_mode="Markdown")

def get_labels(photo_file):
    service = build('vision', 'v1',cache_discovery=False)

    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults':10
                }]
            }]
        })

    response = service_request.execute()
    return response['responses'][0]['labelAnnotations']

def pretty_labels(photo,name):
    URL = photo.file_path
    save_path = "../photos/"+str(name)+".jpg"
    urllib.urlretrieve(URL, save_path)
    l = get_labels(save_path)
    print(l)
    response = "I see...\n"
    for result in l:
        response += "*" + result['description'] + "* : " + '{:.1%}'.format(result['score']) + '\n' 
    return response