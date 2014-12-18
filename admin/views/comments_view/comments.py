# coding: utf-8

from admin.filters import ChoiceEqualFilter
from admin.fields import SelectField
from admin.views.base import SqlAlModelView
from admin.templates import comment_link_formatter

from models.comments.comments import Comments
from utils.constants import OBJECT_TYPES


class CommentsModelView(SqlAlModelView):
    model = Comments
    category = u'Комментарии'
    name = u'Комментарии'

    column_list = (
        'user_id', 'text', 'parent_id', 'obj_type',
        'obj_id', 'obj_name', 'link', 'created'
    )

    named_filter_urls = True

    column_filters = (
        'id', 'text', 'user_id', 'obj_id',
        ChoiceEqualFilter(Comments.obj_type, u'Тип объекта', OBJECT_TYPES),
    )

    column_labels = dict(
        user_id=u'ID пользователя', text=u'Текст',
        created=u'Дата создания', parent_id=u'ID родителя',
        obj_type=u'Тип объекта', obj_id=u'ID объекта',
        obj_name=u'Название объекта', link=u'',
    )

    column_choices = dict(
        obj_type=OBJECT_TYPES,
    )

    column_formatters = {
        'link': comment_link_formatter
    }

    form_columns = (
        'user_id', 'text', 'created', 'parent_id',
        'obj_type', 'obj_id', 'obj_name',
    )

    form_overrides = dict(
        obj_type=SelectField,
    )

    form_args = dict(
        obj_type=dict(
            choices=OBJECT_TYPES,
        ),
    )

