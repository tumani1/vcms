# coding: utf-8
from admin.views.base import BaseModelView
from flask.ext.admin.form import fields
from wtforms.fields import PasswordField, StringField
from wtforms_html5 import EmailField

from pytz import common_timezones

from models.users import Users
from models.users.constants import APP_USERS_TYPE_GENDER


class UsersModelView(BaseModelView):
    model = Users
    category = u'Пользователи'
    name = u'Пользователи'

    form_overrides = dict(
        time_zone=fields.Select2Field,
        gender=fields.Select2Field,
        password=PasswordField,
        phone=StringField,
        email=EmailField,
    )

    form_excluded_columns = ('friends', 'partners', 'created', 'last_visit',
                             'userpic_type', 'userpic_id', 'users_values',
                             'users_chat', 'users_extras', 'person', 'social')

    column_labels = dict(city=u'Родной город', firstname=u'Имя', gender=u'Пол',
                         lastname=u'Фамилия', address=u'Адресс',
                         bio=u'Биография', birthdate=u'Дата рождения',
                         time_zone=u'Временная зона', created=u'Дата создания',
                         phone=u'Телефон', last_visit=u'Последний визит')
    column_exclude_list = ('userpic_type', 'userpic_id')

    column_choices = dict(
        gender=APP_USERS_TYPE_GENDER,
    )

    form_args = dict(
        city=dict(
            label=u'Родной город',
        ),
        firstname=dict(
            label=u'Имя',
        ),
        lastname=dict(
            label=u'Фамилия',
        ),
        address=dict(
            label=u'Адресс',
        ),
        bio=dict(
            label=u'Биография',
        ),
        birthdate=dict(
            label=u'Дата рождения',
        ),
        time_zone=dict(
            label=u'Временная зона',
            choices=[(i, i) for i in common_timezones]
        ),
        gender=dict(
            label=u'Пол',
            choices=APP_USERS_TYPE_GENDER,
        ),
        password=dict(
            label=u'Пароль',
        ),
        phone=dict(
            label=u'Телефон',
        ),
    )
