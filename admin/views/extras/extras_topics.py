# coding: utf-8
from admin.views.base import BaseModelView
from models.extras import ExtrasTopics


class TopicsExtrasModelView(BaseModelView):
    model = ExtrasTopics
    category = u'Топики'
    name = u'Дополнительные материлы топиков'

    column_labels = dict(
        extra=u'Дополнительный материал',
        topics=u'Топик',
    )

    column_display_pk = True


