# coding: utf-8
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from sqlalchemy.orm import sessionmaker

from models import engine

admin = Admin(name='NextTV')

Session = sessionmaker(bind=engine)
session = Session()

from models.users import Users
from models.contents import Cities, Countries
admin.add_view(ModelView(Users, session, category=u'Пользователи', name=u'Пользователи'))

admin.add_view(ModelView(Cities, session, category=u'Локации', name=u'Города'))
admin.add_view(ModelView(Countries, session, category=u'Локации', name=u'Страны'))

