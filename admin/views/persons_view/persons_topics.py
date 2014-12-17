# coding: utf-8

from admin.fields import SelectField
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
        role=u'Роль',
    )

    column_list = form_columns = ('persons', 'topic', 'type', 'role', 'description')

    column_choices = dict(
        type=PERSON_TOPIC_TYPE,
    )

    form_overrides = dict(
        type=SelectField
    )

    form_args = dict(
        type=dict(
            choices=PERSON_TOPIC_TYPE,
        ),
    )


