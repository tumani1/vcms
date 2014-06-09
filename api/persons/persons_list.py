# coding: utf-8

from models import db, Persons
from models.topics.constants import TOPIC_TYPE

from utils.validation import validate_list_int, validate_mLimit, validate_string

__all__ = ['get_person_list']


@db
def get_person_list(user, session, **kwargs):
    # Params
    params = {
        'id': None,
        'text': None,
        'is_online': None,
        'is_user': None,
        'limit': None,
        'topic': None,
        '_type': None,
        'session': session,
    }

    if 'id' in kwargs:
        params['id'] = validate_list_int(kwargs['id'])

    if 'text' in kwargs:
        params['text'] = validate_string(kwargs['text'])

    if 'is_online' in kwargs and kwargs['is_online']:
        params['is_online'] = kwargs['is_online']

    if 'is_user' in kwargs and kwargs['is_user']:
        params['is_user'] = kwargs['is_user']

    if 'limit' in kwargs:
        params['limit'] = validate_mLimit(kwargs['limit'])

    if 'topic' in kwargs:
        params['topic'] = validate_string(kwargs['topic'])

        if 'type' in kwargs:
            if kwargs['type'] in dict(TOPIC_TYPE).keys():
                params['_type'] = kwargs['type']

    return {}
