# coding: utf-8
from flask.ext.admin import Admin

from users import UsersRelsModelView, UsersModelView, UsersValuesModelView,\
    UsersSocialModelView, UsersExtrasModelView, UsersTopicsModelView
from tokens import SessionTokenModelView, GlobalTokenModelView
from persons import PersonsModelView, PersonsUsersModelView,\
    PersonsValuesModelView, PersonsExtrasModelView, PersonsTopicsModelView
from extras import ExtrasModelView, TopicsExtrasModelView
from scheme import SchemeModelView
from topics import TopicsModelView
from cdn import CdnModelView
from chats import ChatsModelView, UsersChatModelView
from locations import CountryModelView, CitieModelView
from stream import StreamModelView
from media import MediaModelView

admin_view = Admin(name='NextTV')

###############################################################################
# Users

admin_view.add_view(UsersModelView())
admin_view.add_view(UsersRelsModelView())
admin_view.add_view(UsersSocialModelView())
admin_view.add_view(UsersValuesModelView())
admin_view.add_view(UsersExtrasModelView())
admin_view.add_view(UsersTopicsModelView())
###############################################################################

###############################################################################
# Token

admin_view.add_view(SessionTokenModelView())
admin_view.add_view(GlobalTokenModelView())
###############################################################################

###############################################################################
# Persons

admin_view.add_view(PersonsModelView())
admin_view.add_view(PersonsUsersModelView())
admin_view.add_view(PersonsValuesModelView())
admin_view.add_view(PersonsExtrasModelView())
admin_view.add_view(PersonsTopicsModelView())
###############################################################################

###############################################################################
# Extras

admin_view.add_view(ExtrasModelView())
###############################################################################

###############################################################################
# Scheme

admin_view.add_view(SchemeModelView())
###############################################################################

###############################################################################
# Topics

admin_view.add_view(TopicsModelView())
admin_view.add_view(TopicsExtrasModelView())
###############################################################################

###############################################################################
# CDN

admin_view.add_view(CdnModelView())
###############################################################################

###############################################################################
# Stream

admin_view.add_view(StreamModelView())
###############################################################################

###############################################################################
# Chats

admin_view.add_view(ChatsModelView())
admin_view.add_view(UsersChatModelView())
###############################################################################

###############################################################################
# Contents

admin_view.add_view(CitieModelView())
admin_view.add_view(CountryModelView())
###############################################################################

###############################################################################
# Media

admin_view.add_view(MediaModelView())
###############################################################################