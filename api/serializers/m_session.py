# coding: utf-8
from utils.serializer import DefaultSerializer
from utils.common import datetime_to_unixtime


class mSession(DefaultSerializer):

    __read_fields = {
        'id': "",
        'user_id': "",
        'token': "",
        'created': "",
        'is_active': "",
        'os': "",
        'browser': "",
        'ip_address': "",
        'device': ""
    }

    def transform_created(self, obj):
        return datetime_to_unixtime(obj.created)
