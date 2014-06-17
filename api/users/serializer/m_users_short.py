# coding: utf-8
from utils.serializer import DefaultSerializer

__all__ = ['mUserShort']


# TODO online
class mUserShort(DefaultSerializer):

    __read_fields = {
        'id': '',
        'firstname': '',
        'lastname': '',
        'is_online': '',
    }

    def transform_is_online(self, obj):
        return None

    def transform_person_id(self, obj):
        return obj.person.id

    def to_native(self, obj):
        if obj.person:
            self.__read_fields['person_id'] = ''
        else:
            self.__read_fields.pop('person_id', None)

        return super(mUserShort, self).to_native(obj)

