# coding: utf-8

from flask.ext.admin.form import fields

from admin.views.base import MongoDBModelView
from admin.templates import chat_messages_formatter

from models.mongo import ChatMessages
from models.users import Users
from models.chats import Chats

from utils.connection import get_session

from flask.ext.admin.contrib.mongoengine.ajax import QueryAjaxModelLoader
from flask.ext.admin.model.fields import AjaxSelectField, InlineFieldList
from flask.ext.admin.contrib.mongoengine.fields import ModelFormField



class ChatMessagesModelView(MongoDBModelView):
    model = ChatMessages
    category = u'Чат'
    name = u'Сообщения чатов'
    session = get_session()

    users = list(session.query(Users.id, Users).all())
    chats = list(session.query(Chats.id, Chats).all())

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
        user_id=fields.Select2Field,
        chat_id=fields.Select2Field,
    )

    form_args = dict(
        user_id=dict(
            choices=map(lambda x: [str(x[0]),x[1]], users),
        ),
        chat_id=dict(
            choices=map(lambda x: [str(x[0]),x[1]], chats),
        ),
    )

    # form_ajax_refs = dict(
    #     chat_id=QueryAjaxModelLoader('chat_id', Chats, fields=['description']),
    # )
