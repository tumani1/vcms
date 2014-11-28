# coding: utf-8

from admin.views.base import SqlAlModelView
from models.locations import Countries


class CountryModelView(SqlAlModelView):
    model = Countries
    category = u'Справочники'
    name = u'Страны'

    column_display_pk = True

    named_filter_urls = True

    column_labels = dict(
        id=u'ISO 3166-1 Alpha-2',
        name=u'Название',
        name_orig=u'Оригинальное название',
        description=u'Описание'
    )

    column_filters = (
        'id', 'name',
    )

    form_columns = (
        'id', 'name', 'name_orig', 'description',
    )
