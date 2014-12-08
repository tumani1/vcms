#coding: utf-8
from utils.serializer import DefaultSerializer
from models.media import MediaUnits, Media
from models.persons import Persons
from models.content import Content
from models.mongo import Stream
from models import Topics


from api import serializers
__all__ = ['mNewsSerializer']


class mNewsSerializer(DefaultSerializer):

    __read_fields = {
        'id': '',
        'text': '',
        'published': '',
        'object': '',
        'comments_cnt': '',
    }

    def __init__(self, **kwargs):
        self.object_types = {
            'mu': (MediaUnits, serializers.mMediaUnitsSerializer),
            'm': (Media, serializers.mMediaSerializer),
            'p': (Persons, serializers.mPersonSerializer),
            'c': (Content, serializers.mContentSerializer),
            's': (Stream, serializers.mStraemElement),
            't': (Topics, serializers.mTopicSerializer)
        }
        self.with_obj = kwargs['with_obj'] if 'with_obj' in kwargs else False
        self.fields = self.__read_fields
        super(mNewsSerializer, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

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