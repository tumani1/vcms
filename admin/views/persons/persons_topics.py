# coding: utf-8
from flask.ext.admin.form import fields

from admin.views.base import SqlAlModelView
from models.topics import PersonsTopics
from models.topics.constants import PERSON_TOPIC_TYPE


class PersonsTopicsModelView(SqlAlModelView):
    model = PersonsTopics
    category = u'Персоны'
    name = u'Топики персоны'

    column_labels = dict(
        persons=u'Персоны',
        description=u'Описание',
        topic=u'Топик',
        type=u'Тип',
    )

    column_choices = dict(
        type=PERSON_TOPIC_TYPE,
    )

    form_overrides = dict(
        type=fields.Select2Field
    )

    form_args = dict(
        type=dict(
            choices=PERSON_TOPIC_TYPE,
        ),
    )


