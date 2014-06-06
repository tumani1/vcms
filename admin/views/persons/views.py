# coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView


class PersonsModelView(ModelView):
    column_labels = dict(country=u'Страна', name=u'Название',
                         name_orig=u'Оригинальное название',
                         time_zone=u'Временая зона', description=u'Описание')
