# coding: utf-8
from admin.views.base import BaseModelView

from models.contents import Countries


class CountryModelView(BaseModelView):
    model = Countries
    category = u'Локации'
    name = u'Страны'

    column_labels = dict(name=u'Название', name_orig=u'Оригинальное название',
                         description=u'Описание')

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
