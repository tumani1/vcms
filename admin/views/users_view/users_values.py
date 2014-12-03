# coding: utf-8
from admin.views.base import SqlAlModelView

from models.users import UsersValues
from wtforms.fields import StringField


class UsersValuesModelView(SqlAlModelView):
    model = UsersValues
    category = u'Пользователи'
    name = u'Дополнительная информация'

    column_list = (
        'user', 'scheme', 'value_int', 'value_text', 'value_string',
    )

    column_labels = dict(
        scheme=u'Схема', user=u'Пользователь',
        value_int=u'Значение (целое число)',
        value_text=u'Значени (текст)',
        value_string=u'Значение (строка)'
    )

    form_columns = (
        'user', 'scheme', 'value_int', 'value_text', 'value_string',
    )

    form_overrides = dict(
        value_text=StringField,
    )

    form_ajax_refs = dict(
        user={
            'fields': ('firstname','lastname',),
        },
        scheme={
            'fields': ('name',),
        },
    )
