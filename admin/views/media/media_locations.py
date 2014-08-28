# coding: utf-8
from admin.views.base import SqlAlModelView
from models.media.media_locations import MediaLocations


class MediaLocationsModelView(SqlAlModelView):
    model = MediaLocations
    category = u'Медиа-объекты'
    name = u'Отношение локаций и медиа'

    column_list = form_columns = ('cdn', 'media', 'quality', 'access_level', 'value',)

    column_labels = dict(
        cdn=u'Идентификатор CDN',
        media=u'Идентификатор медиа',
        quality=u'Качество',
        access_level=u'Уровень доступа',
        value=u'Значение',
    )

