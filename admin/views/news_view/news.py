# coding: utf-8

from admin.views.base import SqlAlModelView
from admin.fields import CKTextAreaField, SelectField
from models.news import News
from utils.constants import OBJECT_TYPES


class NewsModelView(SqlAlModelView):
    model = News
    category = u'Новости'
    name = u'Новости'

    column_list = ('id', 'comments_cnt', 'published', 'created', 'text', 'obj_id', 'obj_name', 'obj_type')

    column_formatters = dict(
        text=lambda v, c, m, p: m.text[0:257]
    )

    column_labels = dict(
        comments_cnt=u"Кол-во комментариев", published=u"Публикация", created=u"Дата создания",
        text=u"Текст", obj_id=u"Id объекта", obj_name=u"Название объекта", obj_type=u"Тип объекта", title=u"Заголовок"
    )

    column_choices = dict(
        obj_type=OBJECT_TYPES
    )

    form_columns = ('title', 'published', 'text', 'obj_id', 'obj_name', 'obj_type')

    form_overrides = dict(
        obj_type=SelectField,
        text=CKTextAreaField,
    )

    form_args = dict(
        obj_type=dict(
            choices=OBJECT_TYPES,
        )
    )