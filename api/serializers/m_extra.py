# coding: utf-8
from utils.common import detetime_to_unixtime as convert_date
from utils.serializer import DefaultSerializer

__all__ = ['mExtra']


class mExtra(DefaultSerializer):

    __read_fields = {
        'id': '',
        'type': '',
        'title': '',
        'title_orig': '',
        'description': '',
        'location': '',
        'created': '',

    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields
        super(mExtra, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_type(self, instance, **kwargs):
        return instance.type.value

    def transform_title(self, instance, **kwargs):
        return instance.title

    def transform_description(self, instance, **kwargs):
        return instance.description

    def transform_title_orig(self, instance, **kwargs):
        return instance.title_orig

    def transform_location(self, instance, **kwargs):
        return instance.location

    def transform_created(self, instance, **kwargs):
        if instance.created is None:
            return None
        return convert_date(instance.created)

