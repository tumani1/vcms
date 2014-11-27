# coding: utf-8

import argparse

from flask import Flask
from flask.ext import login
from flask.ext.mongoengine import MongoEngine

from admin import session
from admin.views import admin_view

from models.users import Users

from settings import DATABASE


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='host', default='127.0.0.1')
    parser.add_argument('--port', dest='port', default=5000)
    parser.add_argument('--no-debug', dest='debug', action='store_false', default=True)
    args = parser.parse_args()

    # Setup Flask app
    app = Flask(__name__, template_folder='admin/templates')
    app.config['SECRET_KEY'] = 'rNAZvhgmFdKkt4dF3CHiooLPCIXxswkYpbQa'
    app.config['MONGODB_SETTINGS'] = DATABASE['mongodb']

    # Setup manager
    login_manager = login.LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(lambda user_id: session.query(Users).get(user_id))

    # Setup MongoDB
    db = MongoEngine()
    db.init_app(app)

    admin_view.init_app(app)

    # Run Flask admin
    app.run(**vars(args))
