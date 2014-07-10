# coding: utf-8
from mongoengine import Document, DateTimeField, StringField, IntField, BinaryField, DictField, SequenceField, signals
import datetime

from constant import APP_STREAM_TYPE


class Stream(Document):
    id          = SequenceField(primary_key=True, verbose_name=u'Id')
    created     = DateTimeField(verbose_name=u'Дата создания', default=datetime.datetime.utcnow)
    type        = StringField(verbose_name=u'Тип', max_length=10, choices=APP_STREAM_TYPE, )
    object      = DictField(verbose_name=u'Объект')
    text        = StringField(verbose_name=u'Текст', default=None)
    user_id     = IntField(verbose_name=u'Пользователь')
    attachments = BinaryField(verbose_name=u'Приложение объекта')

    @classmethod
    def mLimitId(cls, elements, limit):
        if limit:
            if limit['id_dwn'] != 0 and limit['id_top'] != 0:
                elements = elements.filter(id__lte=limit['id_top'], id_gte=['id_dwn'])
            elif limit['id_dwn'] != 0:
                elements = elements.filter(id_gte=['id_dwn'])
            else:
                elements = elements.filter(id_lte=['id_top'])
            top, down = limit['top'], limit['limit']
            if top and down:
                elements = elements[top:down]
            elif top:
                elements = elements[top:]
            else:
                elements = elements[:down]
        return elements

    def __repr__(self):
        return u'<Stream([{}]:type={},user={})>'.format(self.id, self.type, self.user_id)