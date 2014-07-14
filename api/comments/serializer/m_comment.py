# coding: utf-8

from utils.serializer import DefaultSerializer
__all__ = ['mCommentSerializer']

class mCommentSerializer(DefaultSerializer):

    __read_fields = {
        'id': '',
        'user': '',
        'text': '',
        'object': '',
        'relation': '',
    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields
        super(mCommentSerializer, self).__init__(**kwargs)

    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_user(self, instance, **kwargs):
        return ''

    def transform_text(self, instance, **kwargs):
        return instance.text

    def transform_object(self, instance, **kwargs):
        return ''

    def transform_relation(self, instance, **kwargs):
        return ''