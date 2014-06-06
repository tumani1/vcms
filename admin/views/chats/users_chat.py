# coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView

from models.chats.constants import APP_USERSCHAT_TYPE


class UsersChatModelView(ModelView):
    column_labels = dict(chat=u'Чат', user=u'Пользователь', cuStatus=u'Статус',
                         last_update=u'Последнее обновление',)

    column_choices = dict(
        cuStatus=APP_USERSCHAT_TYPE,
    )

    form_choices = dict(
        cuStatus=APP_USERSCHAT_TYPE,
    )

    form_excluded_columns = ('last_update', )