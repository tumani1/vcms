# coding: utf-8
from admin.views.base import SqlAlModelView
from flask.ext.admin.form import fields

from models.users import UsersRels
from models.users.constants import APP_USERSRELS_TYPE, \
    APP_USERSRELS_TYPE_BLOCKED, APP_USERSRELS_BLOCK_TYPE_UNDEF


class UsersRelsModelView(SqlAlModelView):
    model = UsersRels
    category = u'Пользователи'
    name = u'Отношения пользователей'

    column_list = (
        'user', 'partner', 'urStatus', 'blocked', 'updated',
    )

    column_choices = dict(
        urStatus=APP_USERSRELS_TYPE,
        blocked=APP_USERSRELS_TYPE_BLOCKED,
    )

    column_labels = dict(
        user=u'Пользователь', partner=u'Партнёр',
        urStatus=u'Тип отношений', blocked=u'Статус блокировки',
        updated=u'Последнее обновление',
    )

    form_columns = (
        'user', 'partner', 'urStatus', 'blocked', 'updated',
    )

    form_overrides = dict(
        urStatus=fields.Select2Field,
        blocked=fields.Select2Field,
    )

    form_args = dict(
        urStatus=dict(
            choices=APP_USERSRELS_TYPE,
        ),
        blocked=dict(
            choices=APP_USERSRELS_TYPE_BLOCKED,
            default=APP_USERSRELS_BLOCK_TYPE_UNDEF,
        ),
    )

    form_excluded_columns = (
        'updated',
    )

    form_ajax_refs = dict(
        user={
            'fields': ('firstname', 'lastname',),
        },
        partner={
            'fields': ('firstname', 'lastname',),
        },
    )
