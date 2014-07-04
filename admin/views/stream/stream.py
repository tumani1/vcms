# coding: utf-8
from admin.views.base import MongoDBModelView
from models.mongo.stream import Stream


class StreamModelView(MongoDBModelView):
    model = Stream
    name = u'Поток'
    category = u'Поток'

    object_id_converter = int
    form_excluded_columns = ('id', )

    column_labels = dict(
        created=u'Дата создания', type=u'Тип', text=u'Техт',
        user_id=u'Пользователь')

