# coding: utf-8

from flask.ext.admin.form import fields

from admin.filters import ChoiceEqualFilter
from admin.views.base import SqlAlModelView
from admin.templates import topic_link_formatter
from admin.fields import CKTextAreaField

from models.topics import Topics
from models.topics.constants import TOPIC_STATUS, TOPIC_TYPE


class TopicsModelView(SqlAlModelView):
    model = Topics
    category = u'Топики'
    name = u'Топик'

    named_filter_urls = True

    column_filters = (
        'name', 'title',
        ChoiceEqualFilter(Topics.status, u'Статус', TOPIC_STATUS),
        ChoiceEqualFilter(Topics.type, u'Тип', TOPIC_TYPE),
    )

    column_list = (
        'name', 'title', 'status', 'type', 'link', 'releasedate',
    )

    column_choices = dict(
        status=TOPIC_STATUS,
        type=TOPIC_TYPE,
    )

    column_labels = dict(
        name=u'Название',
        title=u'Заголовок',
        title_orig=u'Оригинальное название',
        description=u'Описание',
        status=u'Статус',
        type=u'Тип',
        link=u'',
        releasedate=u'Дата релиза',
    )

    column_formatters = {
        'link': topic_link_formatter
    }

    form_columns = (
        'name', 'title', 'title_orig', 'releasedate',
        'status', 'type', 'description',
    )

    form_overrides = dict(
        status=fields.Select2Field,
        type=fields.Select2Field,
        description=CKTextAreaField,
    )

    form_args = dict(
        status=dict(
            choices=TOPIC_STATUS,
        ),
        type=dict(
            choices=TOPIC_TYPE,
        ),
    )