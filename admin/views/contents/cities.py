# coding: utf-8
from admin.views.base import SqlAlModelView
from flask.ext.admin.form import fields

from models.contents import Cities
from pytz import common_timezones


class CitieModelView(SqlAlModelView):
    model = Cities
    category = u'Локации'
    name = u'Города'

    form_overrides = dict(
        time_zone=fields.Select2Field
    )

    column_labels = dict(country=u'Страна', name=u'Название',
                         name_orig=u'Оригинальное название',
                         time_zone=u'Временая зона', description=u'Описание')

    form_args = dict(
        country=dict(
            label=u'Страна'
        ),
        name=dict(
            label=u'Название',
        ),
        name_orig=dict(
            label=u'Оригинальное название'
        ),
        time_zone=dict(
            label=u'Временная зона',
            choices=[(i, i) for i in common_timezones]
        ),
        description=dict(
            label=u'Описание'
        )
    )

    form_excluded_columns = ('users', )