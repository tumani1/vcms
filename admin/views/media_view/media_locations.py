# coding: utf-8

from admin.views.base import SqlAlModelView
from models.media.media_locations import MediaLocations


class MediaLocationsModelView(SqlAlModelView):
    model = MediaLocations
    category = u'Медиа-объекты'
    name = u'Локации медиа'

    named_filter_urls = True

    column_list = ('cdn', 'media', 'quality', 'access_level', 'value',)

    column_labels = dict(
        cdn=u'CDN',
        media=u'ID медиа',
        quality=u'Качество',
        access_level=u'Уровень доступа',
        value=u'Значение',
    )

    column_filters = (
        'media.title', 'media.owner_id', 'cdn.name', 'quality',
    )

    form_columns = ('cdn', 'media', 'quality', 'access_level', 'value',)

    form_ajax_refs = dict(
        cdn={
            'fields': ('name',),
        },
        media={
            'fields': ('title',),
        },
    )

