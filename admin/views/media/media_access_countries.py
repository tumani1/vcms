# coding: utf-8
from admin.views.base import SqlAlModelView
from models.media.media_access_countries import MediaAccessCountries


class MediaAccessCountriesModelView(SqlAlModelView):
    model = MediaAccessCountries
    category = u'Медиа-объекты'
    name = u'Доступ к медиа по стране'

    column_list = form_columns = ('media', 'location',)

    column_labels = dict(
        media=u'Идентификатор медиа',
        location=u'Идентификатор страны',
    )