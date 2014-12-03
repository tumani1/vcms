# coding: utf-8
from admin.views.base import SqlAlModelView
from models.msgr.msgr_threads import MsgrThreads


class MsgrThreadsModelView(SqlAlModelView):
    model = MsgrThreads
    category = u'Сообщения'
    name = u'Нити сообщений'

    column_list = ('msg_cnt',)
    form_excluded_columns = ('msg_cnt', 'msgr_thread_logs', 'users_msgr_threads')
    column_labels = dict(
        msg_cnt=u'Кол-во сообщений',
    )
