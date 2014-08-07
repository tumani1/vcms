# coding: utf-8
from flask import Flask
from flask.ext.mongoengine import MongoEngine

from views import admin
from settings import DATABASE

import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='host', default='127.0.0.1')
    parser.add_argument('--port', dest='port', default=5000)
    parser.add_argument('--no-debug', dest='debug', action='store_false', default=True)
    args = parser.parse_args()
    app = Flask(__name__)
    db = MongoEngine()
    app.config['MONGODB_SETTINGS'] = DATABASE['mongodb']
    db.init_app(app)
    admin.init_app(app)
    app.run(**vars(args))