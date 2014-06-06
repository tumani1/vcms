# coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.form import fields

from models.users.constants import APP_USERSRELS_TYPE


class UsersRelsModelView(ModelView):
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
