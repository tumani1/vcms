# coding: utf-8

from admin.fields import SelectField
from admin.views.base import SqlAlModelView
from models.msgr.constants import TYPE_STATUS
from models.msgr.users_msgr_threads import UsersMsgrThreads


class UsersMsgrThreadsModelView(SqlAlModelView):
    model = UsersMsgrThreads
    category = u'Сообщения'
    name = u'Отношение пользователей и нитей сообщений'

    column_list = ('users', 'msgr_threads', 'umtStatus', 'last_msg_sent', 'last_visit', 'new_msgs', )
    form_columns = ('users', 'msgr_threads', 'umtStatus',)
    column_labels = dict(
        users=u'Идентификатор пользователя',
        msgr_threads=u'Идентификатор нити',
        umtStatus=u'Статус',
        last_msg_sent=u'Дата последнего сообщения',
        last_visit=u'Дата последнего визита',
        new_msgs=u'Кол-во новых сообщений',
    )

    form_overrides = dict(
        umtStatus=SelectField,
    )

    column_choices = dict(
        umtStatus=TYPE_STATUS,
    )

    form_args = dict(
        umtStatus=dict(
            choices=TYPE_STATUS,
        ),
    )