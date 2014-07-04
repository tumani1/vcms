# coding: utf-8
from flask.ext.admin.form import fields

from admin.views.base import SqlAlModelView
from models.extras import Extras
from models.extras.constants import APP_EXTRA_TYPE


class ExtrasModelView(SqlAlModelView):
    model = Extras

    category = u'Дополнительно'
    name = u'Дополнительные материалы'

    column_list = ('id', 'cdn', 'title', 'title_orig', 'type', 'location',
                   'created', 'description', )

    column_choices = dict(
        type=APP_EXTRA_TYPE,
    )

    column_labels = dict(title=u'Название',
                         title_orig=u'Оригинальное название',
                         type=u'Тип',
                         location=u'Локация',
                         created=u'Дата создания',
                         description=u'Описание',
                         )

    form_overrides = dict(
        type=fields.Select2Field,
    )

    form_excluded_columns = ('created', 'users_extras')

    form_args = dict(
        type=dict(
            label=u'Тип',
            choices=APP_EXTRA_TYPE
        )
    )