# coding: utf-8

from jinja2 import Markup

from flask import url_for
from flask.ext.admin.form import fields

from admin.filters import ChoiceEqualFilter
from admin.views.base import SqlAlModelView
from admin.templates import DROPDOWN_TEMPLATE, UL_TEMPLATE

from models.comments.comments import Comments
from models.comments.constants import OBJECT_TYPES


def _comment_formatter(view, context, model, name):
    action = [
        UL_TEMPLATE % (url_for('users.index_view', flt1_0=model.id), u'Пользователь'),
        UL_TEMPLATE % (url_for('chats.index_view', flt1_0=model.id), u'Объект')
    ]

    return Markup(DROPDOWN_TEMPLATE % ''.join(action))


class CommentsModelView(SqlAlModelView):
    model = Comments
    category = u'Комментарии'
    name = u'Комментарии'

    column_list = (
        'user_id', 'text', 'parent_id', 'obj_type', 'obj_id', 'obj_name', 'action', 'created'
    )

    named_filter_urls = True

    column_filters = (
        'id', 'text', 'user_id', 'obj_id',
        ChoiceEqualFilter(Comments.obj_type, u'Тип объекта', OBJECT_TYPES),
    )

    column_labels = dict(
        user_id=u'ID пользователя',
        text=u'Текст',
        created=u'Дата создания',
        parent_id=u'ID родителя',
        obj_type=u'Тип объекта',
        obj_id=u'ID объекта',
        obj_name=u'Название объекта',
        action=u'',
    )

    column_choices = dict(
        obj_type=OBJECT_TYPES,
    )

    column_formatters = {
        'action': _comment_formatter
    }

    form_columns = (
        'user_id', 'text', 'created', 'parent_id', 'obj_type', 'obj_id', 'obj_name',
    )

    form_overrides = dict(
        obj_type=fields.Select2Field,
    )

    form_args = dict(
        obj_type=dict(
            choices=OBJECT_TYPES,
        ),
    )

