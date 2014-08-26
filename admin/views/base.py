# coding: utf-8
from flask.ext.admin.contrib import sqla, mongoengine
from flask.ext import login
from admin import session


class BaseModelView(object):
    model = None
    name = None
    category = None
    endpoint = None
    url = None

    @classmethod
    def get_model(cls):
        return cls.model


class SqlAlModelView(sqla.ModelView, BaseModelView):

    def __init__(self):
        super(SqlAlModelView, self).__init__(self.model, session, self.name, self.category, self.endpoint, self.url)

    def is_accessible(self):
        return login.current_user.is_authenticated()


class MongoDBModelView(mongoengine.ModelView, BaseModelView):

    def __init__(self):
        super(MongoDBModelView, self).__init__(self.model, self.name, self.category, self.endpoint, self.url)

    def is_accessible(self):
        return login.current_user.is_authenticated()