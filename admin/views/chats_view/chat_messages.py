# coding: utf-8

from sqlalchemy.sql.functions import concat

from admin.fields import select_factory
from admin.views.base import MongoDBModelView
from admin.templates import chat_messages_formatter

from models.mongo import ChatMessages
from models.users import Users
from models.chats import Chats

from utils.connection import get_session


class ChatMessagesModelView(MongoDBModelView):
    model = ChatMessages
    category = u'Чат'
    name = u'Сообщения чатов'
    session = get_session()

    users = list(session.query(Users.id, concat(Users.firstname, ' ', Users.lastname)).all())
    chats = list(session.query(Chats.id, Chats.name).all())

    object_id_converter = True

    column_list = (
        'id', 'user_id', 'chat_id', 'text', 'link', 'created',
    )

    column_formatters = {
        'link': chat_messages_formatter,
    }

    named_filter_urls = True

    column_labels = dict(
        text=u'Текст сообщения',
        created=u'Дата создания',
        user_id=u'Пользователь',
        chat_id=u'Чат',
        link=u'',
    )

    column_choices = dict(
        user_id=users,
        chat_id=chats,
    )

    column_filters = (
        'user_id', 'chat_id', 'text',
    )

    form_excluded_columns = ('id', )

    form_columns = (
        'id', 'user_id', 'chat_id', 'created', 'text',
    )

    form_overrides = dict(
        user_id=select_factory(coerce=int),
        chat_id=select_factory(coerce=int),
    )

    form_args = dict(
        user_id=dict(
            choices=users,
        ),
        chat_id=dict(
            choices=chats,
        ),
    )