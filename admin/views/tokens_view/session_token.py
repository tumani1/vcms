# coding: utf-8
from admin.views.base import SqlAlModelView
from models.tokens import SessionToken


class SessionTokenModelView(SqlAlModelView):
    model = SessionToken
    category = u'Токены пользователя'
    name = u'Токен сэссии'

    column_list = (
        'token', 'users', 'is_active', 'created'
    )

    column_labels = dict(
        token=u'Токен',
        users=u'Пользователь',
        created=u'Дата создания',
        is_active=u'Активность'
    )

    column_filters = (
        'users.id', 'users.firstname', 'users.lastname', 'is_active',
    )

    form_columns = (
        'users', 'is_active',
    )

    form_ajax_refs = dict(
        users={
            'fields': ('firstname', 'lastname', ),
        },
    )