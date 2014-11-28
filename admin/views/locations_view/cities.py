# coding: utf-8

from pytz import common_timezones

from flask.ext.admin.form import fields

from admin.views.base import SqlAlModelView
from models.locations import Cities


class CitieModelView(SqlAlModelView):
    model = Cities
    category = u'Справочники'
    name = u'Города'

    form_overrides = dict(
        time_zone=fields.Select2Field
    )

    column_labels = dict(
        country=u'Страна', name=u'Название',
        name_orig=u'Оригинальное название',
        time_zone=u'Временая зона', description=u'Описание'
    )

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

    form_columns = (
        'country', 'name', 'name_orig',
        'region', 'time_zone', 'description',
    )

    form_ajax_refs = dict(
        country={
            'fields': ('name',),
        },
    )
