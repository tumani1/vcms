# coding: utf-8
from admin.views.base import BaseModelView

from models.users import UsersValues
from wtforms.fields import StringField


class UsersValuesModelView(BaseModelView):
    model = UsersValues
    category = u'Пользователи'
    name = u'Дополнительная информация'

    form_overrides = dict(
        value_text=StringField,
    )

    column_labels = dict(
        scheme=u'Схема', user=u'Пользователь',
        value_int=u'Значение (целое число)', value_text=u'Значени (текст)',
        value_string=u'Значение (строка)'
    )
