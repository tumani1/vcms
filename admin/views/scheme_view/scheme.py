# coding: utf-8
from flask.ext.admin.form import fields

from admin.views.base import SqlAlModelView
from models.scheme import Scheme
from models.scheme.constants import KLASS_TYPE


class SchemeModelView(SqlAlModelView):
    model = Scheme
    category = u'Схема'
    name = u'Схема'

    form_overrides = dict(
        klass=fields.Select2Field,
    )

    column_choices = dict(
        klass=KLASS_TYPE,
    )

    form_excluded_columns = ('users_value', )

    form_args = dict(
        klass=dict(
            choices=KLASS_TYPE
        )
    )