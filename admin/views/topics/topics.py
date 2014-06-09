# coding: utf-8
from admin.views.base import BaseModelView
from models.topics import Topics


class TopicsModelView(BaseModelView):
    model = Topics
    category = u'Топики'
    name = u'Топик'


