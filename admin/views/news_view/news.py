# coding: utf-8

from flask.ext.admin.form import fields

from admin.views.base import SqlAlModelView
from models.news import News
from utils.constants import OBJECT_TYPES


class NewsModelView(SqlAlModelView):
    model = News
    category = u'Новости'
    name = u'Новости'

    column_list = ('id', 'comments_cnt', 'published', 'created', 'text', 'obj_id', 'obj_name', 'obj_type')

    column_labels = dict(
        comments_cnt=u"Кол-во комментариев", published=u"Публикация", created=u"Дата создания",
        text=u"Текст", obj_id=u"Id объекта", obj_name=u"Название объекта", obj_type=u"Тип объекта", title=u"Заголовок"
    )

    column_choices = dict(
        obj_type=OBJECT_TYPES
    )

    form_columns = ('comments_cnt', 'published', 'created', 'text', 'obj_id', 'obj_name', 'obj_type', 'title')

    form_overrides = dict(
        obj_type=fields.Select2Field,
    )

    form_args = dict(
        obj_type=dict(
            choices=OBJECT_TYPES,
        )
    )