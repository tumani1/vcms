# coding: utf-8
from admin.views.base import SqlAlModelView
from models.media.media_units_access_countries import MediaUnitsAccessCountries


class MediaUnitsAccessCountriesModelView(SqlAlModelView):
    model = MediaUnitsAccessCountries
    category = u'Медиа-объекты'
    name = u'Доступ к медиа-юниту по стране'

    column_list = form_columns = ('media_units', 'location',)

    column_labels = dict(
        media_units=u'Идентификатор медиа-юнита',
        location=u'Идентификатор страны',
    )