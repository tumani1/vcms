# coding: utf-8

from flask.ext.admin.form import fields

from admin.views.base import SqlAlModelView
from admin.filters import ChoiceEqualFilter
from admin.templates import person_link_formatter

from models.persons import Persons
from models.persons.constants import APP_PERSONS_STATUS_TYPE


class PersonsModelView(SqlAlModelView):
    model = Persons
    category = u'Персоны'
    name = u'Персоны'

    named_filter_urls = True

    column_filters = (
        'id', 'firstname', 'lastname', 'users.id', 'users.firstname', 'users.lastname',
        ChoiceEqualFilter(Persons.status, u'Статус', APP_PERSONS_STATUS_TYPE)
    )

    column_list = (
        'id', 'firstname', 'lastname', 'status', 'bio', 'link', 'users'
    )

    column_labels = dict(
        firstname=u'Имя',
        lastname=u'Фамилия',
        status=u'Статус персоны',
        bio=u'Биография',
        users=u'Пользователь',
        link=u''
    )

    column_formatters = {
        'link': person_link_formatter
    }

    form_columns = (
        'firstname', 'lastname', 'status', 'bio', 'users',
    )

    form_overrides = dict(
        status=fields.Select2Field
    )

    form_args = dict(
        status=dict(
            choices=APP_PERSONS_STATUS_TYPE,
        ),
    )
