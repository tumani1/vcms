# coding: utf-8

from utils.serializer import DefaultSerializer


class mMsgrThread(DefaultSerializer):

    __read_fields = {
        'id': '',
        'msgr_cnt': '',
        'users': '',

    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields

        super(mMsgrThread, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_msgr_cnt(self, instance, **kwargs):
        return instance.msgr_cnt

    def transform_users(self, instance, **kwargs):
        return {}


