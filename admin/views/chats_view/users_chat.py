# coding: utf-8
from flask.ext.admin.form import fields
from admin.views.base import SqlAlModelView

from models.chats import UsersChat
from models.chats.constants import APP_USERSCHAT_TYPE


class UsersChatModelView(SqlAlModelView):
    model = UsersChat
    category = u'Чат'
    name = u'Чаты пользователя'

    column_display_pk = True

    column_list = ('id', 'chat', 'user', 'cuStatus', 'last_update',)

    column_labels = dict(
        chat=u'Чат',
        user=u'Пользователь',
        cuStatus=u'Статус',
        last_update=u'Последнее обновление',
    )

    column_choices = dict(
        cuStatus=APP_USERSCHAT_TYPE,
    )

    form_columns = ('chat', 'user', 'cuStatus', )

    form_excluded_columns = ('last_update', )

    form_choices = dict(
        cuStatus=APP_USERSCHAT_TYPE,
    )

    form_ajax_refs = dict(
        chat={
            'fields': ('description',),
        },
        user={
            'fields': ('firstname', 'lastname',),
        },
    )
