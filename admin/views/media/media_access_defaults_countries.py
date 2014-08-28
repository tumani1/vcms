# coding: utf-8
from admin.views.base import SqlAlModelView
from models.media.media_access_defaults_countries import MediaAccessDefaultsCountries


class MediaAccessDefaultsCountriesModelView(SqlAlModelView):
    model = MediaAccessDefaultsCountries
    category = u'Медиа-объекты'
    name = u'Доступ к медиа по стране c типом default'

    column_list = form_columns = ('media_type', 'location',)

    column_labels = dict(
        media_type=u'Тип медиа',
        location=u'Идентификатор страны',
    )
