#coding: utf-8

from utils.serializer import DefaultSerializer
from models.media import MediaUnits, Media
from models.persons import Persons
from models.content import Content
from models.mongo import Stream
from models import Topics
from api.serializers.m_media import mMediaSerializer
from api.serializers.m_persons import mPersonSerializer
from api.serializers.m_media_unit import mMediaUnitsSerializer
from api.serializers.m_content import mContentSerializer
from api.serializers.m_topic import mTopicSerializer
from api.serializers.m_stream_element_m_comment import mStreamElement

__all__ = ['mNewsSerializer']


class mNewsSerializer(DefaultSerializer):

    __read_fields = {
        'id': '',
        'title': '',
        'text': '',
        'published': '',
        'object': '',
        'comments_cnt': '',
    }

    def __init__(self, **kwargs):
        self.object_types = {
            'mu': (MediaUnits, mMediaUnitsSerializer),
            'm': (Media, mMediaSerializer),
            'p': (Persons, mPersonSerializer),
            'c': (Content, mContentSerializer),
            's': (Stream, mStreamElement),
            't': (Topics, mTopicSerializer)
        }
        self.with_obj = kwargs['with_obj'] if 'with_obj' in kwargs else False
        self.fields = self.__read_fields
        super(mNewsSerializer, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_title(self, instance, **kwargs):
        return instance.title

    def transform_text(self, instance, **kwargs):
        return instance.text

    def transform_published(self, instance, **kwargs):
        return instance.published

    def transform_comments_cnt(self, instance, **kwargs):
        return instance.comments_cnt

    def transform_object(self, instance, **kwargs):
        if self.with_obj:

            if instance.obj_id:
                if instance.obj_type.code == 's':
                    obj = self.object_types[instance.obj_type.code][0].objects.get(id=instance.obj_id)
                else:
                    obj = self.session.query(self.object_types[instance.obj_type.code][0]).filter_by(id=instance.obj_id).first()
            else:
                obj = self.session.query(self.object_types[instance.obj_type.code][0]).filter_by(name=instance.name).first()
            if instance.obj_type.code == 'c':
                return self.object_types[instance.obj_type.code][1](obj).get_data()
            else:
                params = {
                    'instance': obj,
                    'user': self.user,
                    'session': self.session,
                }
                return self.object_types[instance.obj_type.code][1](**params).data