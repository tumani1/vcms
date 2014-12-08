# coding: utf-8

from flask.ext.admin.form import fields

from admin.views.base import SqlAlModelView
from utils.constants import OBJECT_TYPES
from models.content.content import Content


class ContentModelView(SqlAlModelView):
    model = Content
    category = u'Контент'
    name = u'Контент'

    named_filter_urls = True

    column_filters = (
        'id', 'title',
    )

    column_list = (
        'id', 'title', 'text', 'obj_type', 'obj_id', 'obj_name'
    )

    column_labels = dict(
        title=u'Заголовок',
        text=u'Текст',
        obj_type=u'Тип объекта',
        obj_id=u'Идентификатор объекта',
        obj_name=u'Название объекта',
    )

    column_choices = dict(
        obj_type=OBJECT_TYPES,
    )

    form_columns = (
        'title', 'text', 'obj_type', 'obj_id', 'obj_name'
    )

    form_overrides = dict(
        obj_type=fields.Select2Field,
    )

    form_args = dict(
        obj_type=dict(
            choices=OBJECT_TYPES,
        ),
    )




