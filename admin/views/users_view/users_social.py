# coding: utf-8
from admin.views.base import SqlAlModelView
from flask.ext.admin.form import fields

from models.users import UsersSocial
from models.users.constants import APP_USERSOCIAL_TYPE


class UsersSocialModelView(SqlAlModelView):
    model = UsersSocial
    category = u'Пользователи'
    name = u'Социальные сети'

    column_list = ('user', 'sType', 'sToken', 'created', 'updated', )

    column_choices = dict(
        sType=APP_USERSOCIAL_TYPE,
    )

    column_labels = dict(
        user=u'Пользователь', sType=u'Социальная сеть',
        sToken=u'Токен пользователя', created=u'Дата создания',
        updated=u'Последнее обновление',
    )

    form_columns = (
        'user', 'sType', 'sToken',
    )

    form_overrides = dict(
        sType=fields.Select2Field
    )

    form_args = dict(
        sType=dict(
            choices=APP_USERSOCIAL_TYPE,
        )
    )

    form_ajax_refs = dict(
        user={
            'fields': ('firstname', 'lastname',),
        },
    )
