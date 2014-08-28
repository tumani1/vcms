# coding: utf-8
from flask.ext.admin.form import fields
from admin.views.base import SqlAlModelView
from models.media.media_units import MediaUnits
from models.media.constants import APP_MEDIA_LIST


class MediaUnitsModelView(SqlAlModelView):
    model = MediaUnits
    category = u'Медиа-объекты'
    name = u'Медиа unit'

    form_columns = column_list = ('title', 'title_orig', 'topic_name', 'description', 'previous_unit', 'next_unit', 'release_date',
                                  'end_date', 'batch', 'access', 'access_type' )

    column_labels = dict(
        title=u'Заголовок',
        title_orig=u'Оригинальное название',
        topic_name=u'Топик',
        description=u'Описание',
        previous_unit=u'Предыдущий unit',
        next_unit=u'Следующий unit',
        release_date=u'Дата выхода',
        end_date=u'Дата окончания',
        batch=u'Серия',
        access=u'Доступ',
        access_type=u'Тип доступа',
    )

    form_overrides = dict(
        access_type=fields.Select2Field,
    )

    column_choices = dict(
        access_type=APP_MEDIA_LIST,
    )

    form_args = dict(
        access_type=dict(
            choices=APP_MEDIA_LIST,
        ),
    )


