# coding: utf-8

from admin.views.base import SqlAlModelView
from flask.ext.admin.form import fields

from models.persons import Persons
from models.persons.constants import APP_PERSONS_STATUS_TYPE


class PersonsModelView(SqlAlModelView):
    model = Persons
    category = u'Персоны'
    name = u'Персоны'

    column_list = (
        'firstname', 'lastname', 'status', 'bio', 'users',
    )

    column_labels = dict(
        firstname=u'Имя',
        lastname=u'Фамилия',
        status=u'Статус персоны',
        bio=u'Биография',
        users=u'Пользователь'
    )

    column_filters = (
        'id', 'users.id',
        #'firstname', 'lastname',
    )

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
