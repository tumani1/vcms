# coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.form import fields

from pytz import common_timezones


class CitieModelView(ModelView):
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