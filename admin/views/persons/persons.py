# coding: utf-8
from admin.views.base import SqlAlModelView
from flask.ext.admin.form import fields

from models.persons import Persons
from models.persons.constants import APP_PERSONS_STATUS_TYPE


class PersonsModelView(SqlAlModelView):
    model = Persons
    category = u'Персоны'
    name = u'Персоны'

    form_overrides = dict(
        status=fields.Select2Field
    )

    column_labels = dict(firstname=u'Имя', lastname=u'Фамилия',
                         status=u'Статус персоны',
                         bio=u'Биография', users=u'Пользователь')

    column_list = ('firstname', 'lastname', 'status', 'bio', 'users')

    form_columns = column_list

    form_args = dict(
        firstname=dict(
            label=u'Имя',
        ),
        lastname=dict(
            label=u'Фамилия',
        ),
        status=dict(
            label=u'Статус персоны',
            choices=APP_PERSONS_STATUS_TYPE,
        ),
        bio=dict(
            label=u'Биография',
        ),
        users=dict(
            label=u'Пользователь'
        ),
    )
