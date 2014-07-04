# coding: utf-8
from flask.ext.admin.contrib import sqla, mongoengine

from utils.connection import get_session


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

    def __init__(self, session=get_session()):
        super(SqlAlModelView, self).__init__(self.model, session, self.name, self.category, self.endpoint, self.url)


class MongoDBModelView(mongoengine.ModelView, BaseModelView):

    def __init__(self):
        super(MongoDBModelView, self).__init__(self.model, self.name, self.category, self.endpoint, self.url)