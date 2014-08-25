# coding: utf-8
from admin.views.base import SqlAlModelView

from models.users import UsersValues
from wtforms.fields import StringField


class UsersValuesModelView(SqlAlModelView):
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

    form_columns = column_list = ('user', 'scheme', 'value_int', 'value_text',
                                  'value_string', )
