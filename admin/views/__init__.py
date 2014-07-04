# coding: utf-8
from flask.ext.admin import Admin

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
from stream import StreamModelView

admin = Admin(name='NextTV')

###############################################################################
# Users

admin.add_view(UsersModelView())
admin.add_view(UsersRelsModelView())
admin.add_view(UsersSocialModelView())
admin.add_view(UsersValuesModelView())
admin.add_view(UsersExtrasModelView())
admin.add_view(UsersTopicsModelView())
###############################################################################

###############################################################################
# Token

admin.add_view(SessionTokenModelView())
admin.add_view(GlobalTokenModelView())
###############################################################################

###############################################################################
# Persons

admin.add_view(PersonsModelView())
admin.add_view(PersonsUsersModelView())
admin.add_view(PersonsValuesModelView())
admin.add_view(PersonsExtrasModelView())
admin.add_view(PersonsTopicsModelView())
###############################################################################

###############################################################################
# Extras

admin.add_view(ExtrasModelView())
###############################################################################

###############################################################################
# Scheme

admin.add_view(SchemeModelView())
###############################################################################

###############################################################################
# Topics

admin.add_view(TopicsModelView())
admin.add_view(TopicsExtrasModelView())
###############################################################################

###############################################################################
# CDN

admin.add_view(CdnModelView())
###############################################################################

###############################################################################
# Stream

admin.add_view(StreamModelView())
###############################################################################

###############################################################################
# Chats

admin.add_view(ChatsModelView())
admin.add_view(UsersChatModelView())
###############################################################################

###############################################################################
# Contents

admin.add_view(CitieModelView())
admin.add_view(CountryModelView())
###############################################################################