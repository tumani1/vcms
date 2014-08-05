# coding: utf-8

from utils.serializer import DefaultSerializer

__all__ = ['mLocationSerializer']


class mLocationSerializer(DefaultSerializer):

    __read_fields = {
        'id': '',
        'quality': '',
        'CDN_name': '',
        'value': '',
    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields
        super(mLocationSerializer, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_quality(self, instance, **kwargs):
        return instance.quality

    def transform_CDN_name(self, instance, **kwargs):
        return instance.cdn_name

    def transform_value(self, instance, **kwargs):
        return instance.value