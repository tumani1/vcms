# coding: utf-8
from admin.views.base import BaseModelView

from models.chats import UsersChat
from models.chats.constants import APP_USERSCHAT_TYPE


class UsersChatModelView(BaseModelView):
    model = UsersChat
    category = u'Чат'
    name = u'Чаты пользователя'

    column_labels = dict(chat=u'Чат', user=u'Пользователь', cuStatus=u'Статус',
                         last_update=u'Последнее обновление',)

    column_choices = dict(
        cuStatus=APP_USERSCHAT_TYPE,
    )

    form_choices = dict(
        cuStatus=APP_USERSCHAT_TYPE,
    )

    form_excluded_columns = ('last_update', )