# coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView


class BaseModelView(ModelView):
    model = None
    name = None
    category = None
    endpoint = None
    url = None

    def __init__(self, session):
        model = self.model
        name = self.name
        category = self.category
        endpoint = self.endpoint
        url = self.url
        super(BaseModelView, self).__init__(model, session, name, category, endpoint, url)

    @classmethod
    def get_model(cls):
        return cls.model
