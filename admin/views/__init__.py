# coding: utf-8

from flask.ext.admin import Admin
from sqlalchemy.orm import sessionmaker

from connectors import db_connect

admin = Admin(name='NextTV')

engine = db_connect()
session = sessionmaker(bind=engine)()

###############################################################################
# User
from users import UsersRelsModelView, UsersModelView
from models.users import UsersRels, Users

admin.add_view(UsersRelsModelView(UsersRels, session, category=u'Пользователи', name=u'Отношения пользователей'))
admin.add_view(UsersModelView(Users, session, category=u'Пользователи', name=u'Пользователи'))
###############################################################################

###############################################################################
# Contents
from contents import CountryModelView, CitieModelView
from models.contents import Countries, Cities

admin.add_view(CitieModelView(Cities, session, category=u'Локации', name=u'Города'))
admin.add_view(CountryModelView(Countries, session, category=u'Локации', name=u'Страны'))
###############################################################################
