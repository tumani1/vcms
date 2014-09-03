# coding: utf-8
from utils.serializer import DefaultSerializer


class mAttach(DefaultSerializer):

    __read_fields = {
        'type': '',
        'id': '',
        'id_str': '',
    }

    def __init__(self, **kwargs):
        super(DefaultSerializer, self).__init__(**kwargs)

    def transform_type(self, obj):
        return ''

    def transform_id(self, obj):
        return 1

    def transform_id_str(self, obj):
        return ''

    def transform_object(self, obj):
        return {}