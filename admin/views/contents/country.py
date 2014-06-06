# coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView


class CountryModelView(ModelView):

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
