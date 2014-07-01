# coding: utf-8

from utils.serializer import DefaultSerializer

__all__ = ['mMediaSerializer']


class mMediaSerializer(DefaultSerializer):

    __read_fields = {
        'id': '',
        'title': '',
        'title_orig': '',
        'description': '',
        'releasedate': '',
        'duration': '',
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
        return instance.release_date

    def transform_duration(self, instance, **kwargs):
        return  instance.duration