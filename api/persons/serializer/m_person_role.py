# coding: utf-8

from utils.serializer import DefaultSerializer
from utils.common import group_by

from models.users.users import Users

__all__ = ['mPersonRoleSerializer']


class mPersonRoleSerializer(DefaultSerializer):
    __read_fields = {
        'id': '',
        'firstname': '',
        'lastname': '',
        'user': '',
        'role': '',
        'type': '',
        'relation': '',
    }

    def __init__(self, **kwargs):
        self.fields = self.__read_fields

        keys = ['person', 'topic_name', 'role', 'type']
        kwargs['instance'] = [dict(zip(keys, item)) for item in kwargs['instance']]

        super(mPersonRoleSerializer, self).__init__(**kwargs)

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
           user_list = [item['person'].user_id for item in obj if not item['person'].user_id is None]
           person_list = [item['person'].id for item in obj]

        self.list_user_id = user_list
        self.list_person_id = person_list


    def transform_id(self, instance, **kwargs):
        return instance['person'].id

    def transform_firstname(self, instance, **kwargs):
        return instance['person'].firstname

    def transform_lastname(self, instance, **kwargs):
        return instance['person'].lastname

    def transform_user(self, instance, **kwargs):
        return {}

    def transform_role(self, instance, **kwargs):
        return instance['role']

    def transform_type(self, instance, **kwargs):
        return instance['type'].code

    def transform_relation(self, instance, **kwargs):
        user_id = instance['person'].user_id
        if self.is_auth and not user_id is None:
            result = self.up.get(user_id, False)

            if result and not result[0].user_persons is None:
                return {
                    'liked': result[0].user_persons.check_liked,
                    'subscribed': result[0].user_persons.check_subscribed,
                }

        return {}
