#!/usr/bin/env python
import os
import sys

# Adding lib folder, that is created locally,
#   to the Path so we can use external libraries on Google App Engine

# To install packages here with pip,
#   run pip install -t path/to/lib -r requirements.txt

sys.path.append(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'lib'))

import hook_handler
from bot_token import TOKEN
from webapp2 import Route, WSGIApplication

# Setting the valid routes for our simple web application.

routes = [
    # Route for setting webhook
    Route('/set_webhook', handler='hook_handler.WebHookHandler:set_webhook'),

    # Route for Telegram updates
    Route('/' + TOKEN, handler='hook_handler.WebHookHandler:webhook_handler')
]

app = WSGIApplication(routes, debug=False)
