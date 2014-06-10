# coding: utf-8

from utils.serializer import DefaultSerializer
from utils.common import group_by

from models.users.users import Users

__all__ = ['mPersonSerializer']


class mPersonSerializer(DefaultSerializer):

    __read_fields = {
        'id': '',
        'firstname': '',
        'lastname': '',
        'user': '',
        'relation': '',
    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields

        super(mPersonSerializer, self).__init__(**kwargs)

        # Calc
        self.calc_list_user_id()

        params = {
            'session': self.session,
            'user_id': self.list_user_id,
            'person_id': self.list_person_id,
        }

        result = Users.get_user_by_person(**params).all()
        self.up = group_by(result, 'id', True)


    def calc_list_user_id(self):
        user_list = []
        person_list = []

        obj = self.instance

        if hasattr(obj, '__iter__'):
           user_list = [item.user_id for item in obj if not item.user_id is None]
           person_list = [item.id for item in obj]
        else:
            person_list.append(obj.id)

            if not obj is None and not obj.user_id is None:
                user_list.append(obj.user_id)

        self.list_user_id = user_list
        self.list_person_id = person_list


    def transform_id(self, instance, **kwargs):
        return instance.id

    def transform_firstname(self, instance, **kwargs):
        return instance.firstname

    def transform_lastname(self, instance, **kwargs):
        return instance.lastname

    def transform_user(self, instance, **kwargs):
        return {}

    def transform_relation(self, instance, **kwargs):
        user_id = instance.user_id
        if self.is_auth and not user_id is None:
            result = self.up.get(user_id, False)

            if result and not result[0].user_persons is None:
                return {
                    'liked': result[0].user_persons.check_liked,
                    'subscribed': result[0].user_persons.check_subscribed,
                }

        return {}
