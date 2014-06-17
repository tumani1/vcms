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
        if not kwargs['instance'] is None:
            key = ['topic', 'user', 'subscribed', 'liked']
            if isinstance(kwargs['instance'], list):
                kwargs['instance'] = [dict(zip(key, item)) for item in kwargs['instance']]
            else:
                kwargs['instance'] = dict(zip(key, kwargs['instance']))

        super(mTopicSerializer, self).__init__(**kwargs)


    def transform_name(self, instance, **kwargs):
        return instance['topic'].name


    def transform_title(self, instance, **kwargs):
        return instance['topic'].title


    def transform_title_orig(self, instance, **kwargs):
        return instance['topic'].title_orig


    def transform_description(self, instance, **kwargs):
        return instance['topic'].description


    def transform_releasedate(self, instance, **kwargs):
        return instance['topic'].get_unixtime_created


    def transform_type(self, instance, **kwargs):
        return instance['topic'].type.code


    def transform_relation(self, instance, **kwargs):
        if self.is_auth:
            return {
                'liked': UsersPersons.cls_check_liked(instance['liked']),
                'subscribed': UsersPersons.cls_check_subscribed(instance['subscribed']),
            }

        return {}
