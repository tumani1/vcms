# coding: utf-8
from flask.ext.admin.form import fields

from admin.views.base import SqlAlModelView
from models.topics import Topics
from models.topics.constants import TOPIC_STATUS, TOPIC_TYPE


class TopicsModelView(SqlAlModelView):
    model = Topics
    category = u'Топики'
    name = u'Топик'

    # form_excluded_columns = ('topic_values', 'topic_user', )
    form_columns = ('name', 'title', 'title_orig', 'description', 'releasedate',
                    'status', 'type', )
    column_exclude_list = ('search_description', )

    column_display_pk = True

    column_choices = dict(
        status=TOPIC_STATUS,
        type=TOPIC_TYPE,
    )

    column_labels = dict(
        name=u'Название',
        title=u'Заголовок',
        title_orig=u'Оригинальное название',
        description=u'Описание',
        releasedate=u'Дата релиза',
        status=u'Статус',
        type=u'Тип',
    )

    form_overrides = dict(
        status=fields.Select2Field,
        type=fields.Select2Field,
    )

    form_args = dict(
        status=dict(
            choices=TOPIC_STATUS,
        ),
        type=dict(
            choices=TOPIC_TYPE,
        ),
    )
