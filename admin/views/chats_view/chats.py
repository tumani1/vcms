# coding: utf-8
from admin.views.base import SqlAlModelView

from models.chats import Chats


class ChatsModelView(SqlAlModelView):
    model = Chats
    category = u'Чат'
    name = u'Чаты'

    column_display_pk = True

    column_labels = dict(
        description=u'Дескриптор чата'
    )

    form_columns = ('description', )
