# coding: utf-8

from utils.serializer import DefaultSerializer
from models.users.users import Users

__all__ = ['mPersonSerializer']


class mPersonSerializer(DefaultSerializer):

    __read_keys = {
        'id': '',
        'firstname': '',
        'lastname': '',
        'user': '',
        'relation': '',
    }

    def __init__(self, instance, user, **kwargs):
        super(mPersonSerializer, self).__init__(instance, user, **kwargs)

        # Calc
        self.calc_list_user_id()
        # Users.get_user_with_person()


    def calc_list_user_id(self):
        result = []
        obj = self.instance

        if hasattr(obj, '__iter__'):
           result = [item.user_id for item in obj if not item.user_id is None]
        else:
            if not obj is None and not obj.user_id is None:
                result.append(obj.user_id)

        self.list_user_id = result


    def get_id(self, instance, **kwargs):
        return instance.id

    def get_firstname(self, instance, **kwargs):
        return instance.firstname

    def get_lastname(self, instance, **kwargs):
        return instance.lastname

    def get_user(self, instance, **kwargs):
        return ''

    def get_relation(self, instance, **kwargs):
        if self.is_auth:
            return {
                'liked': '',
                'subscribed': '',
            }

        return {}
