# coding: utf-8

from utils.serializer import DefaultSerializer

from models.users.users import Users
from models.persons.persons_users import UsersPersons

__all__ = ['mTopicSerializer']


class mTopicSerializer(DefaultSerializer):

    __read_fields = {
        'name': '',
        'title': '',
        'title_orig': '',
        'description': '',
        'releasedate': '',
        'type': '',
        'relation': '',
    }


    def __init__(self, **kwargs):
        super(mTopicSerializer, self).__init__(**kwargs)


    def transform_name(self, instance, **kwargs):
        return instance.name


    def transform_title(self, instance, **kwargs):
        return instance.title


    def transform_title_orig(self, instance, **kwargs):
        return instance.title_orig


    def transform_description(self, instance, **kwargs):
        return instance.title_orig


    def transform_releasedate(self, instance, **kwargs):
        return instance.title_orig


    def transform_type(self, instance, **kwargs):
        return instance.type.code


    def transform_relation(self, instance, **kwargs):
        user_id = instance.user_id
        if self.is_auth and not user_id is None:
            user_person = self.up.get("{0}-{1}".format(instance.id, instance.user_id), False)

            if user_person:
                return {
                    'liked': UsersPersons.cls_check_liked(user_person['liked']),
                    'subscribed': UsersPersons.cls_check_subscribed(user_person['subscribed']),
                }

        return {}
