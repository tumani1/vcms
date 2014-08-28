# coding: utf-8
from admin.views.base import SqlAlModelView
from models.tags.tags import Tags


class TagsModelView(SqlAlModelView):
    model = Tags
    category = u'Тэги'
    name = u'Тэги'

    column_list = form_columns = ('name', 'status', 'type',)
    column_labels = dict(
        name=u'Название',
        status=u'Статус',
        type=u'Тип',
    )



