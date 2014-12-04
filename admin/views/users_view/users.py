# coding: utf-8

from pytz import common_timezones

from flask.ext.admin.form import fields

from wtforms.fields import PasswordField
from wtforms_html5 import EmailField, TelField, TelInput, TextField, _Input

from admin.filters import ChoiceEqualFilter, IsPersonFilterEqual, PhoneFilter
from admin.views.base import SqlAlModelView
from admin.templates import user_link_formatter
from admin.admin_validators import custom_phone_validator

from models.users import Users
from models.users.constants import APP_USERS_TYPE_GENDER, APP_USER_STATUS_TYPE


class MyTelInput(_Input):
    input_type = "tel"

    def __call__(self, field, **kwargs):
        if hasattr(field.data, 'e164'):
            kwargs['value'] = field.data.e164

        return _Input.__call__(self, field, **kwargs)


class UsersModelView(SqlAlModelView):
    model = Users
    category = u'Пользователи'
    name = u'Пользователи'

    column_labels = dict(
        city=u'Родной город', firstname=u'Имя', gender=u'Пол',
        lastname=u'Фамилия', address=u'Адресс', birthdate=u'Дата рождения',
        time_zone=u'Временная зона', created=u'Дата создания',
        phone=u'Телефон', last_visit=u'Последний визит', link=u'',
        status=u'Статус',
    )

    column_list = (
        'id', 'firstname', 'lastname', 'gender', 'email',
        'city', 'is_manager', 'address', 'phone', 'birthdate',
        'time_zone', 'link', 'created', 'last_visit', 'status',
    )

    column_choices = {
        'gender': APP_USERS_TYPE_GENDER,
        'status': APP_USER_STATUS_TYPE,
    }

    column_formatters = {
        'link': user_link_formatter,
    }

    named_filter_urls = True

    column_filters = (
        'id', 'firstname', 'lastname', 'city.id', 'city.name',
        'city.region', 'city.country.name',
        ChoiceEqualFilter(Users.status, u'Статус', APP_USER_STATUS_TYPE),
        IsPersonFilterEqual(Users.filter_users_person, Users.id, u'Персона', (('1', u'Yes'),)),
        PhoneFilter(Users.phone, u'Телефон'),
    )

    form_overrides = dict(
        time_zone=fields.Select2Field,
        gender=fields.Select2Field,
        status=fields.Select2Field,
        password=PasswordField,
        phone=TelField,
        email=EmailField,
    )

    form_columns = (
        'firstname', 'lastname', 'gender', 'status', 'password',
        'email', 'city', 'is_manager', 'address', 'bio', 'phone',
        'birthdate', 'time_zone', 'created', 'last_visit',
    )

    form_args = dict(
        time_zone=dict(
            label=u'Временная зона',
            choices=[(i, i) for i in common_timezones]
        ),
        gender=dict(
            label=u'Пол',
            choices=APP_USERS_TYPE_GENDER,
        ),
        status=dict(
            label=u'Статус',
            choices=APP_USER_STATUS_TYPE,
        ),
        phone=dict(
            widget=MyTelInput(),
            validators=[custom_phone_validator],
        ),
    )

    form_ajax_refs = dict(
        city={
            'fields': ('name',),
        },
    )
