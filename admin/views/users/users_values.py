# coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView

from wtforms.fields import StringField


class UsersValuesModelView(ModelView):
    form_overrides = dict(
        value_text=StringField,
    )

    column_labels = dict(
        scheme=u'Схема', user=u'Пользователь',
        value_int=u'Значение (целое число)', value_text=u'Значени (текст)',
        value_string=u'Значение (строка)'
    )
