# coding: utf-8
from admin.views.base import SqlAlModelView
from models.msgr.msgr_log import MsgrLog


class MsgrLogModelView(SqlAlModelView):
    model = MsgrLog
    category = u'Сообщения'
    name = u'Сообщения'

    column_list = ('msgr_threads', 'users', 'created', 'text', 'attachments', )
    form_columns = ('msgr_threads', 'users', 'text', 'attachments', )
    column_labels = dict(
        msgr_threads=u'Идентификатор нити',
        users=u'Идентификатор пользователя',
        created=u'Дата создания',
        text=u'Текст',
        attachments=u'Прикрепленный объект',
    )


