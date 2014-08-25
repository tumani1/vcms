# coding: utf-8
from mongoengine import Document, StringField, IntField, SequenceField, DateTimeField
from datetime import datetime


class ChatMessages(Document):
    id      = SequenceField(primary_key=True)
    text    = StringField(verbose_name=u'Текст сообщения')
    created = DateTimeField(verbose_name=u'Дата создания', default=datetime.utcnow())
    user_id = IntField(verbose_name=u'Пользователь')
    chat_id = IntField(verbose_name=u'Чат')