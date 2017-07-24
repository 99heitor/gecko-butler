#!/usr/bin/env python

import os
import sys
import json
from webapp2 import Route, WSGIApplication

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))

import hook_handler


with open('keys/bot_token.json') as json_data:
    data = json.load(json_data)
    TOKEN = data['token']

routes = [
    # Route for handle webhook (change it using admin rights, maybe..
    Route('/set_webhook', handler='hook_handler.WebHookHandler:set_webhook'),

    # Route for Telegram updates
    Route('/' + TOKEN, handler='hook_handler.WebHookHandler:webhook_handler')
]
app = WSGIApplication(routes, debug=False)
