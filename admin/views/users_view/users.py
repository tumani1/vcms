# coding: utf-8

from pytz import common_timezones

from jinja2 import Markup
from flask import url_for
from flask.ext.admin.form import fields

from wtforms.fields import PasswordField, StringField
from wtforms_html5 import EmailField

from admin.views.base import SqlAlModelView
from admin.templates import DROPDOWN_TEMPLATE, UL_TEMPLATE

from models.users import Users
from models.users.constants import APP_USERS_TYPE_GENDER


def _user_formatter(view, context, model, name):
    action = [
        UL_TEMPLATE % (url_for('comments.index_view', flt1_0=model.id), u'Комментарии'),
        UL_TEMPLATE % (url_for('chats.index_view', flt1_0=model.id), u'Сообщения в чате')
    ]

    if False:
        action.append(UL_TEMPLATE % (url_for('persons.index_view', flt1_0=model.id), u'Персона'))

    return Markup(DROPDOWN_TEMPLATE % ''.join(action))


class UsersModelView(SqlAlModelView):
    model = Users
    category = u'Пользователи'
    name = u'Пользователи'

    column_labels = dict(
        city=u'Родной город', firstname=u'Имя', gender=u'Пол',
        lastname=u'Фамилия', address=u'Адресс', birthdate=u'Дата рождения',
        time_zone=u'Временная зона', created=u'Дата создания',
        phone=u'Телефон', last_visit=u'Последний визит',
        action=u''
    )

    column_list = (
        'id', 'firstname', 'lastname', 'gender', 'email',
        'city', 'is_manager', 'address', 'phone', 'birthdate',
        'time_zone', 'action', 'created', 'last_visit',
    )

    column_choices = dict(
        gender=APP_USERS_TYPE_GENDER,
    )

    column_formatters = {
        'action': _user_formatter
    }

    named_filter_urls = True

    column_filters = (
        'id', 'firstname', 'lastname', #'phone', #'status', 'country', 'is_person'
    )

    form_overrides = dict(
        time_zone=fields.Select2Field,
        gender=fields.Select2Field,
        password=PasswordField,
        phone=StringField,
        email=EmailField,
    )

    form_columns = (
        'firstname', 'lastname', 'gender', 'password', 'email',
        'city', 'is_manager', 'address', 'bio', 'phone',
        'birthdate', 'time_zone', 'created', 'last_visit'
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
    )

    # # form_excluded_columns = ('password',)
    #
    # def scaffold_form(self):
    #     form_class = super(UsersModelView, self).scaffold_form()
    #     form_class.password2 = PasswordField('New Password')
    #     return form_class
    #
    # # def on_model_create(self, **kwargs):
    # #     print "ok"
    # #     pass
    # #
    # def on_model_change(self, form, model, **kwargs):
    #     # self.form_overrides
    #     if len(model.password2):
    #         model.password = form.password2.data
    #
    # def edit_form(self, obj=None):
    #     super(UsersModelView, self).edit_form(obj)

