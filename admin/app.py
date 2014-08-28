# coding: utf-8
from flask import Flask, render_template
from flask.ext import login
from flask.ext.mongoengine import MongoEngine

from views import admin_view
from admin import session
from models.users import Users
from settings import DATABASE

import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='host', default='127.0.0.1')
    parser.add_argument('--port', dest='port', default=5000)
    parser.add_argument('--no-debug', dest='debug', action='store_false', default=True)
    args = parser.parse_args()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'rNAZvhgmFdKkt4dF3CHiooLPCIXxswkYpbQa'
    login_manager = login.LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(lambda user_id: session.query(Users).get(user_id))

    db = MongoEngine()
    app.config['MONGODB_SETTINGS'] = DATABASE['mongodb']
    db.init_app(app)
    admin_view.init_app(app)
    app.run(**vars(args))