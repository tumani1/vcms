# coding: utf-8
from utils.serializer import DefaultSerializer
from models.scheme.constants import M_SCHEME_STR, M_SCHEME_TXT


class mValue(DefaultSerializer):

    __read_fields = {
        'name': '',
        'value': '',
    }


    def transform_name(self, obj):
        return obj.id


    def transform_value(self, obj):
        if obj.scheme.klass.code == M_SCHEME_TXT:
            return obj.value_text
        elif obj.scheme.klass.code == M_SCHEME_STR:
            return obj.value_string
        else:
            return obj.value_int

