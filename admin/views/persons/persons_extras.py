# coding: utf-8
from flask.ext.admin.form import fields

from admin.views.base import SqlAlModelView
from models.extras import PersonsExtras
from models.extras.constants import APP_PERSONS_EXTRA_TYPE, \
    APP_PERSONS_EXTRA_TYPE_NULL


class PersonsExtrasModelView(SqlAlModelView):
    model = PersonsExtras
    category = u'Персоны'
    name = u'Дополнительные материлы'

    form_overrides = dict(
        extra_type=fields.Select2Field,
    )

    column_choices = dict(
        extra_type=APP_PERSONS_EXTRA_TYPE,
    )

    column_labels = dict(
        extra_type=u'Тип доп. материала',
        extra=u'Дополнительный материал',
        persons=u'Персона',
    )

    form_columns = column_list = ('persons', 'extra', 'extra_type', )

    form_args = dict(
        extra_type=dict(
            choices=APP_PERSONS_EXTRA_TYPE,
            default=APP_PERSONS_EXTRA_TYPE_NULL,
        ),
    )