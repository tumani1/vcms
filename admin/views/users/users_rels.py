# coding: utf-8
from admin.views.base import SqlAlModelView
from flask.ext.admin.form import fields

from models.users import UsersRels
from models.users.constants import APP_USERSRELS_TYPE


class UsersRelsModelView(SqlAlModelView):
    model = UsersRels
    category = u'Пользователи'
    name = u'Отношения пользователей'

    form_overrides = dict(
        urStatus=fields.Select2Field
    )

    column_choices = dict(
        urStatus=APP_USERSRELS_TYPE,
    )

    column_labels = dict(user=u'Пользователь', partner=u'Партнёр',
                         urStatus=u'Тип отношений',
                         updated=u'Последнее обновление')

    form_args = dict(
        user=dict(
            label=u'Пользователь'
        ),
        partner=dict(
            label=u'Партнёры'
        ),
        urStatus=dict(
            label=u'Тип отношений',
            choices=APP_USERSRELS_TYPE,
        ),

    )

    form_excluded_columns = ('updated', )
