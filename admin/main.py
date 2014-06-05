# coding: utf-8
from flask import Flask

from views import admin


def start_application(host='127.0.0.1', port=5000, debug=True):
    app = Flask(__name__)
    admin.init_app(app)
    app.run(debug=debug, port=port, host=host)