# coding: utf-8
from utils.serializer import DefaultSerializer
from utils.common import datetime_to_unixtime as convert_date
from api.serializers.m_localion import mLocationSerializer

__all__ = ['mMediaSerializer']


class mMediaSerializer(DefaultSerializer):

    __read_fields = {
        'id': '',
        'title': '',
        'title_orig': '',
        'description': '',
        'releasedate': '',
        'duration': '',
        'relation': '',
        'locations': '',
    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields
        super(mMediaSerializer, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_title(self, instance, **kwargs):
        return instance.title

    def transform_title_orig(self, instance, **kwargs):
        return instance.title_orig

    def transform_description(self, instance, **kwargs):
        return instance.description

    def transform_releasedate(self, instance, **kwargs):
        if instance.release_date:
            return convert_date(instance.release_date)

    def transform_duration(self, instance, **kwargs):
        return instance.duration

    def transform_locations(self, instance, **kwargs):
        return mLocationSerializer(user=None, session=None, instance=instance.media_locations).data

    def transform_relation(self, instance, **kwargs):
        relation = {}
        users_media = instance.users_media
        if self.is_auth and not users_media is None:
            if users_media[0].watched:
                relation.update(watched=convert_date(users_media[0].watched))
            if users_media[0].liked:
                relation.update(liked=convert_date(users_media[0].liked))
            if users_media[0].play_pos:
                relation.update(pos=users_media[0].play_pos)
        return relation
