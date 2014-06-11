# coding: utf-8

from api.persons.persons_list import get_person_list

__all__ = ['get_topic_person']


def get_topic_person(user, name, **kwargs):
    return get_person_list(user=user, topic=name, **kwargs)
