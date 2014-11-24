# coding: utf-8
from flask.ext.admin.form import fields
from admin.views.base import SqlAlModelView
from models.comments.comments import Comments
from models.comments.constants import OBJECT_TYPES


class CommentsModelView(SqlAlModelView):
    model = Comments
    category = u'Комментарии'
    name = u'Комментарии'

    column_list = form_columns = ('user_id', 'text', 'created', 'parent_id', 'obj_type', 'obj_id', 'obj_name',)

    column_labels = dict(
        user_id=u'Идентификатор пользователя',
        text=u'Текст',
        created=u'Дата создания',
        parent_id=u'Идентификатор родителя',
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

