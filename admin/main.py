# coding: utf-8
from flask import Flask

from views import admin


if __name__ == '__main__':
    app = Flask(__name__)
    admin.init_app(app)
    app.run(debug=True)