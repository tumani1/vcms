# coding: utf-8

from flask.ext.admin import Admin
from sqlalchemy.orm import sessionmaker

from utils.db_engine import db_connect


admin = Admin(name='NextTV')

engine = db_connect()
session = sessionmaker(bind=engine)()

###############################################################################
# User
from users import UsersRelsModelView, UsersModelView, UsersValuesModelView,\
    UsersSocialModelView, UsersExtrasModelView

admin.add_view(UsersModelView(session))
admin.add_view(UsersRelsModelView(session))
admin.add_view(UsersSocialModelView(session))
admin.add_view(UsersValuesModelView(session))
admin.add_view(UsersExtrasModelView(session))
###############################################################################

###############################################################################
# Token
from tokens import SessionTokenModelView, GlobalTokenModelView

admin.add_view(SessionTokenModelView(session))
admin.add_view(GlobalTokenModelView(session))
###############################################################################

###############################################################################
# Persons
from persons import PersonsModelView

admin.add_view(PersonsModelView(session))
###############################################################################

###############################################################################
# Extras
from extras import ExtrasModelView

admin.add_view(ExtrasModelView(session))
###############################################################################

###############################################################################
# Scheme
from scheme import SchemeModelView

admin.add_view(SchemeModelView(session))
###############################################################################

###############################################################################
# Topics
from topics import TopicsModelView

admin.add_view(TopicsModelView(session))
###############################################################################

###############################################################################
# CDN
from cdn import CdnModelView

admin.add_view(CdnModelView(session))
###############################################################################

###############################################################################
# Chats
from chats import ChatsModelView, UsersChatModelView

admin.add_view(ChatsModelView(session))
admin.add_view(UsersChatModelView(session))
###############################################################################

###############################################################################
# Contents
from contents import CountryModelView, CitieModelView

admin.add_view(CitieModelView(session))
admin.add_view(CountryModelView(session))
###############################################################################