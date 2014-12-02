# coding: utf-8

import argparse

from flask import Flask
from flask.ext import login, admin
from flask.ext.mongoengine import MongoEngine

from admin import session as db_session
from admin.views import *

from models.users import Users

from settings import DATABASE


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='host', default='127.0.0.1')
    parser.add_argument('--port', dest='port', default=5000)
    parser.add_argument('--no-debug', dest='debug', action='store_false', default=True)
    args = parser.parse_args()

    ###############################################################################
    # Setup Flask app
    app = Flask(__name__, template_folder='admin/templates')
    app.config['SECRET_KEY'] = 'rNAZvhgmFdKkt4dF3CHiooLPCIXxswkYpbQa'
    app.config['MONGODB_SETTINGS'] = DATABASE['mongodb']

    ###############################################################################
    # Setup manager
    login_manager = login.LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(lambda user_id: db_session.query(Users).get(user_id))

    ###############################################################################
    # Setup MongoDB
    db = MongoEngine()
    db.init_app(app)

    ###############################################################################
    # Setup callbacks
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if not exception is None:
            db_session.remove()

    ###############################################################################
    # Admin
    admin_view = admin.Admin(name='NextTV', index_view=AdminIndexView(), base_template='admin_master.html')

    ###############################################################################
    # Users
    admin_view.add_view(UsersModelView())

    ###############################################################################
    # Persons
    admin_view.add_view(PersonsModelView())

    ###############################################################################
    # Topics
    admin_view.add_view(TopicsModelView())

    ###############################################################################
    # Chats
    admin_view.add_view(ChatsModelView())
    admin_view.add_view(ChatMessagesModelView())

    ###############################################################################
    # Extras
    admin_view.add_view(ExtrasModelView())

    ###############################################################################
    # Scheme
    admin_view.add_view(SchemeModelView())

    ###############################################################################
    # Dictionary
    admin_view.add_view(CdnModelView())
    admin_view.add_view(CitieModelView())
    admin_view.add_view(CountryModelView())

    ###############################################################################
    # Stream
    admin_view.add_view(StreamModelView())

    ###############################################################################
    # Media
    admin_view.add_view(MediaModelView())
    admin_view.add_view(MediaUnitsModelView())
    admin_view.add_view(MediaLocationsModelView())
    admin_view.add_view(PersonsMediaModelView())

    ###############################################################################
    # Comments
    admin_view.add_view(CommentsModelView())

    # ###############################################################################
    # # Tags
    # admin_view.add_view(TagsModelView())
    # admin_view.add_view(TagsObjectsModelView())

    ###############################################################################
    # Content
    admin_view.add_view(ContentModelView())

    ###############################################################################
    # Eshop
    admin_view.add_view(ItemsModelView())
    admin_view.add_view(ItemsExtrasModelView())
    admin_view.add_view(ItemsObjectsModelView())
    admin_view.add_view(UsersItemsModelView())
    admin_view.add_view(CategoriesModelView())
    admin_view.add_view(CategoriesExtrasModelView())
    admin_view.add_view(VariantsModelView())
    admin_view.add_view(VariantsExtrasModelView())
    admin_view.add_view(VariantsSchemeModelView())
    admin_view.add_view(VariantsValuesModelView())
    admin_view.add_view(CartsModelView())
    admin_view.add_view(CartLogModelView())
    admin_view.add_view(ItemsCartsModelView())
    admin_view.add_view(PaymentsModelView())

    ###############################################################################
    # Init admin app
    admin_view.init_app(app)

    ###############################################################################
    # Run Flask admin
    app.run(**vars(args))
