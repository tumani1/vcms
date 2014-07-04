# coding: utf-8
from flask import Flask
from flask.ext.mongoengine import MongoEngine

from views import admin
from settings import DATABASE


def start_admin_application(host='127.0.0.1', port=5000, debug=True):
    app = Flask(__name__)
    db = MongoEngine()
    app.config['MONGODB_SETTINGS'] = DATABASE['mongodb']
    db.init_app(app)
    admin.init_app(app)
    app.run(debug=debug, port=port, host=host)