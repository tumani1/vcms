# coding: utf-8

from flask.ext.admin import Admin
from sqlalchemy.orm import sessionmaker

from utils.connectors import db_connect


admin = Admin(name='NextTV')

engine = db_connect()
session = sessionmaker(bind=engine)()

###############################################################################
# User
from users import UsersRelsModelView, UsersModelView, UsersValuesModelView,\
    UsersSocialModelView, UsersExtrasModelView
from models.users import UsersRels, Users, UsersValues, UsersSocial, UsersExtras

admin.add_view(UsersModelView(Users, session, category=u'Пользователи', name=u'Пользователи'))
admin.add_view(UsersRelsModelView(UsersRels, session, category=u'Пользователи', name=u'Отношения пользователей'))
admin.add_view(UsersSocialModelView(UsersSocial, session, category=u'Пользователи', name=u'Социальные сети'))
admin.add_view(UsersValuesModelView(UsersValues, session, category=u'Пользователи', name=u'Дополнительная информация'))
admin.add_view(UsersExtrasModelView(UsersExtras, session, category=u'Пользователи', name=u'Дополнительные материалы'))
###############################################################################

###############################################################################
# Persons
from persons import PersonsModelView
from models.persons import Persons

admin.add_view(PersonsModelView(Persons, session, category=u'Персоны', name=u'Персоны'))
###############################################################################

###############################################################################
# Chats
from chats import ChatsModelView, UsersChatModelView
from models.chats import Chats, UsersChat

admin.add_view(ChatsModelView(Chats, session, category=u'Чат', name=u'Чаты'))
admin.add_view(UsersChatModelView(UsersChat, session, category=u'Чат', name=u'Чаты пользователя'))
###############################################################################

###############################################################################
# Contents
from contents import CountryModelView, CitieModelView
from models.contents import Countries, Cities

admin.add_view(CitieModelView(Cities, session, category=u'Локации', name=u'Города'))
admin.add_view(CountryModelView(Countries, session, category=u'Локации', name=u'Страны'))
###############################################################################