# coding: utf-8
from admin.views.base import SqlAlModelView
from models.persons import PersonsValues

from wtforms.fields import TextField


class PersonsValuesModelView(SqlAlModelView):
    model = PersonsValues
    category = u'Персоны'
    name = u'Дополнительная информация'

    form_overrides = dict(
        value_text=TextField,
    )

    column_labels = dict(
        scheme=u'Схема', persons=u'Персона',
        value_int=u'Значение (целое число)', value_text=u'Значени (текст)',
        value_string=u'Значение (строка)'
    )