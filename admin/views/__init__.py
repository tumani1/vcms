# coding: utf-8

from flask.ext.admin import Admin

from utils.connection import db_connect, create_session

from users import UsersRelsModelView, UsersModelView, UsersValuesModelView,\
    UsersSocialModelView, UsersExtrasModelView
from tokens import SessionTokenModelView, GlobalTokenModelView
from persons import PersonsModelView, PersonsUsersModelView, PersonsValuesModelView
from extras import ExtrasModelView, TopicsExtrasModelView, PersonsExtrasModelView
from scheme import SchemeModelView
from topics import TopicsModelView, PersonsTopicsModelView, UsersTopicsModelView
from cdn import CdnModelView
from chats import ChatsModelView, UsersChatModelView
from contents import CountryModelView, CitieModelView

admin = Admin(name='NextTV')

session = create_session(bind=db_connect(), expire_on_commit=False)

###############################################################################
# Users

admin.add_view(UsersModelView(session))
admin.add_view(UsersRelsModelView(session))
admin.add_view(UsersSocialModelView(session))
admin.add_view(UsersValuesModelView(session))
admin.add_view(UsersExtrasModelView(session))
admin.add_view(UsersTopicsModelView(session))
###############################################################################

###############################################################################
# Token

admin.add_view(SessionTokenModelView(session))
admin.add_view(GlobalTokenModelView(session))
###############################################################################

###############################################################################
# Persons

admin.add_view(PersonsModelView(session))
admin.add_view(PersonsUsersModelView(session))
admin.add_view(PersonsValuesModelView(session))
admin.add_view(PersonsExtrasModelView(session))
admin.add_view(PersonsTopicsModelView(session))
###############################################################################

###############################################################################
# Extras

admin.add_view(ExtrasModelView(session))
###############################################################################

###############################################################################
# Scheme

admin.add_view(SchemeModelView(session))
###############################################################################

###############################################################################
# Topics

admin.add_view(TopicsModelView(session))
admin.add_view(TopicsExtrasModelView(session))
###############################################################################

###############################################################################
# CDN

admin.add_view(CdnModelView(session))
###############################################################################

###############################################################################
# Chats

admin.add_view(ChatsModelView(session))
admin.add_view(UsersChatModelView(session))
###############################################################################

###############################################################################
# Contents

admin.add_view(CitieModelView(session))
admin.add_view(CountryModelView(session))
###############################################################################