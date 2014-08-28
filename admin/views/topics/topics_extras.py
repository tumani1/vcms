# coding: utf-8
from admin.views.base import SqlAlModelView
from models.extras import ExtrasTopics


class TopicsExtrasModelView(SqlAlModelView):
    model = ExtrasTopics
    category = u'Топики'
    name = u'Дополнительные материлы топиков'

    column_labels = dict(
        extra=u'Дополнительный материал',
        topics=u'Топик',
    )

    column_list = form_columns = ('topics', 'extra', 'extra_type', )


