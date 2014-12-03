# coding: utf-8
import datetime
from mongoengine import Document, DateTimeField, StringField, IntField, DictField, SequenceField

from constant import APP_STREAM_TYPE


class Stream(Document):
    id          = SequenceField(primary_key=True, verbose_name=u'Id')
    created     = DateTimeField(verbose_name=u'Дата создания', default=datetime.datetime.utcnow)
    type        = StringField(verbose_name=u'Тип', max_length=10, choices=APP_STREAM_TYPE, )
    object      = DictField(verbose_name=u'Объект')
    text        = StringField(verbose_name=u'Текст')
    user_id     = IntField(verbose_name=u'Пользователь')
    attachments = DictField(verbose_name=u'Приложение объекта')

    @classmethod
    def mLimitId(cls, query, limit):
        if limit:
            if limit['id_dwn'] != 0 and limit['id_top'] != 0:
                query = query.filter(id__lte=limit['id_top'], id_gte=['id_dwn'])
            elif limit['id_dwn'] != 0:
                query = query.filter(id_gte=limit['id_dwn'])
            elif 'id_top' in limit:
                query = query.filter(id_lte=limit['id_top'])
            if 'top' in limit and 'limit' in limit:
                top, down = limit['top'], limit['limit']
                if top and down:
                    query = query[top:down]
                elif top:
                    query = query[top:]
                else:
                    query = query[:down]
        return query

    # Юзеры друзья
    @classmethod
    def signal(cls, type_, user_id=None, **kwargs):
        stream_el = cls(type=type_, object=kwargs.get('object', {}), user_id=user_id, attachments=kwargs.get('attachments', {}))
        stream_el.save()
        return stream_el

    def __repr__(self):
        return u'<Stream([{}]:type={},user={})>'.format(self.id, self.type, self.user_id)