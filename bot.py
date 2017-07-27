# !/usr/bin/env python
import os
import sys
from webapp2 import Route, WSGIApplication

from bot_info import TOKEN, APP_URL

# Adding lib folder, that is created locally,
#   to the Path so we can use external libraries on Google App Engine

# To install packages here with pip,
#   run pip install -t path/to/lib -r requirements.txt

sys.path.append(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'lib'))

# Setting the valid routes for our simple web application.

ROUTES = [
    # Route for setting webhook
    Route('/set_webhook', handler='webhook_setup.WebHookHandler:set_webhook'),

    # Route for Telegram updates
    Route('/' + TOKEN,
          handler='webhook_setup.WebHookHandler:webhook_handler')
]

app = WSGIApplication(ROUTES, debug=False)


if __name__ == "__main__":
    # Execute app on localhost instead of app engine.
    # Be sure to update APP_URL on bot_info.py (not tracked)
    from paste import httpserver
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "vision_key.json"
    httpserver.serve(app, host='127.0.0.1', port='80')

# else:
#     sys.path.append(os.path.join(os.path.dirname(
#         os.path.realpath(__file__)), 'lib'))
