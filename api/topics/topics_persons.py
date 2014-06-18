# coding: utf-8

from api.persons.persons_list import get_person_list

__all__ = ['get_topic_person']


def get_topic_person(auth_user, name, **kwargs):
    return get_person_list(user=auth_user, topic=name, **kwargs)
