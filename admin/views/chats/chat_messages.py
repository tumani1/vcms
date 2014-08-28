# coding: utf-8
from flask.ext.admin.form import fields

from admin.views.base import MongoDBModelView
from models.mongo import ChatMessages
from models.users import Users
from models.chats import Chats
from utils.connection import get_session


class ChatMessagesModelView(MongoDBModelView):
    model = ChatMessages
    category = u'Чат'
    name = u'Сообщения пользователя'
    session = get_session()

    users = list(session.query(Users.id, Users).all())
    chats = list(session.query(Chats.id, Chats).all())

    object_id_converter = True
    form_excluded_columns = ('id', )

    column_labels = dict(text=u'Текст сообщения', created=u'Дата создания',
                         user_id=u'Пользователь', chat_id=u'Чат')

    form_columns = column_list = ('id', 'user_id', 'chat_id', 'created', 'text', )

    form_overrides = dict(
        user_id=fields.Select2Field,
        chat_id=fields.Select2Field
    )

    column_choices = dict(
        user_id=users,
        chat_id=chats,
    )

    form_args = dict(
        user_id=dict(
            choices=users,
        ),
        chat_id=dict(
            choices=chats,
        ),
    )