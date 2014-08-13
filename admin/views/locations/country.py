# coding: utf-8
from admin.views.base import SqlAlModelView

from models.locations import Countries


class CountryModelView(SqlAlModelView):
    model = Countries
    category = u'Локации'
    name = u'Страны'

    column_labels = dict(name=u'Название', name_orig=u'Оригинальное название',
                         description=u'Описание')


    column_display_pk = True

    form_args = dict(
        name=dict(
            label=u'Название'
        ),
        name_orig=dict(
            label=u'Оригинальное название'
        ),
        description=dict(
            label=u'Описание'
        )
    )

    form_excluded_columns = ('cities', )

# coding: utf-8
