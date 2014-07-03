# coding: utf-8
from mongoengine import Document, DateTimeField, StringField, IntField, BinaryField, DictField, signals
import datetime

from constant import APP_STREAM_TYPE


class Stream(Document):
    created     = DateTimeField(verbose_name=u'Дата создания', default=datetime.datetime.utcnow)
    type        = StringField(verbose_name=u'Тип', max_length=10, choices=APP_STREAM_TYPE, )
    object     = DictField(verbose_name=u'Объект')
    text       = StringField(verbose_name=u'Текст', default=None)
    user_id     = IntField(verbose_name=u'Пользователь')
    attachments = BinaryField(verbose_name=u'Приложение объекта')

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if 'created' in kwargs and kwargs['created']:
            document.id = cls.objects.count() + 1

    def __repr__(self):
        return u'<Stream([{}]:type={},user={})>'.format(self.id, self.type, self.user_id)


signals.pre_init.connect(Stream.pre_save, sender=Stream)