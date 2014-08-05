# coding: utf-8

from utils.serializer import DefaultSerializer


class mMsgrMsg(DefaultSerializer):

    __read_fields = {
        'id': '',
        'text': '',
        'user': '',
        'created': '',
        'attach': '',
        'thread': ''

    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields

        super(mMsgrMsg, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_text(self, instance, **kwargs):
        return instance.text

    def transform_attach(self, instance, **kwargs):
        return instance.attach

    def transform_user(self, instance, **kwargs):
        return {}

    def transform_thread(self, instance, **kwargs):
        return {}
