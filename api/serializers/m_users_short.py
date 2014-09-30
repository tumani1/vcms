# coding: utf-8
from utils.serializer import DefaultSerializer
from models.users.constants import APP_USERSRELS_TYPE_UNDEF
from models.users import UsersRels
from models.tokens import SessionToken

__all__ = ['mUserShort']


class mUserShort(DefaultSerializer):

    __read_fields = {
        'id': '',
        'firstname': '',
        'lastname': '',
        'is_online': '',
    }

    def __init__(self, user=None, **kwargs):
        super(mUserShort, self).__init__(user=user, **kwargs)
        if not user is None:
            self.__read_fields['relation'] = ''

    def transform_is_online(self, obj):
        return SessionToken.user_is_online(obj.id, self.session)

    def transform_person_id(self, obj):
        return obj.person.id

    def transform_relation(self, obj):
        if self.user:
            return UsersRels.get_reletion_status(self.user.id, obj.id, self.session)
        else:
            return APP_USERSRELS_TYPE_UNDEF

    def to_native(self, obj):
        if obj.person:
            self.__read_fields['person_id'] = ''
        else:
            self.__read_fields.pop('person_id', None)

        return super(mUserShort, self).to_native(obj)
