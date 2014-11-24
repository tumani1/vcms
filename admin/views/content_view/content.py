# coding: utf-8
from admin.views.base import SqlAlModelView
from models.comments.constants import OBJECT_TYPES
from models.content.content import Content
from flask.ext.admin.form import fields


class ContentModelView(SqlAlModelView):
    model = Content
    category = u'Контент'
    name = u'Контент'

    column_list = form_columns = ('title', 'text', 'obj_type', 'obj_id', 'obj_name')
    column_labels = dict(
        title=u'Заголовок',
        text=u'Текст',
        obj_type=u'Тип объекта',
        obj_id=u'Идентификатор объекта',
        obj_name=u'Название объекта',
    )

    form_overrides = dict(
        obj_type=fields.Select2Field,
    )

    column_choices = dict(
        obj_type=OBJECT_TYPES,
    )

    form_args = dict(
        obj_type=dict(
            choices=OBJECT_TYPES,
        ),
    )




