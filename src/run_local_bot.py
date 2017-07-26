import webapp2
from paste import httpserver
from webapp import app
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "vision_key.json"


def main():
    httpserver.serve(app, host='127.0.0.1', port='80')


if __name__ == '__main__':
    main()
