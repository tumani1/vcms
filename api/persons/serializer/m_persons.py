# coding: utf-8

from api.users.serializer import mUser

from utils.serializer import DefaultSerializer

from models.users.users import Users
from models.persons.persons_users import UsersPersons

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
        super(mPersonSerializer, self).__init__(**kwargs)

        # Calc
        self.calc_list_user_id()

        result = []
        if self.is_auth:
            params = {
                'session': self.session,
                'user': self.user,
                'person_id': self.up_list.keys(),
            }

            result = UsersPersons.get_user_person(**params).all()

        # Find relation
        relation = {}
        for item in result:
            relation[item.person_id] = item

        self.relation = relation

        # Find users
        user_list = {}
        params = {
            'session': self.session,
            'users_id': [item for item in self.up_list.values() if not item is None]
        }

        for item in Users.get_users_by_id(**params).all():
            user_list[item.id] = item

        self.user_list = user_list


    def calc_list_user_id(self):
        up_list = {}
        obj = self.instance

        if hasattr(obj, '__iter__'):
            for item in obj:
                up_list[item.id] = item.user_id

        else:
            up_list[obj.id] = obj.user_id

        self.up_list = up_list


    def transform_id(self, instance, **kwargs):
        return instance.id


    def transform_firstname(self, instance, **kwargs):
        return instance.firstname


    def transform_lastname(self, instance, **kwargs):
        return instance.lastname


    def transform_user(self, instance, **kwargs):
        user_id = instance.user_id
        if not user_id is None:
            user_person = self.user_list.get(user_id, False)
            if user_person:
                return mUser(instance=user_person, session=self.session, user=self.user).data

        return {}


    def transform_relation(self, instance, **kwargs):
        if self.is_auth:
            user_person = self.relation.get(instance.id, False)

            if user_person:
                return {
                    'liked': user_person.check_liked,
                    'subscribed': user_person.check_subscribed,
                }

        return {}
