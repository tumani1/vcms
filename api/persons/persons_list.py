# coding: utf-8

from models.persons import Persons
from models.topics.constants import TOPIC_TYPE

from utils.validation import validate_list_int, validate_mLimit, validate_string
from api.serializers import mPersonSerializer, mPersonRoleSerializer

__all__ = ['get_person_list']


def get_person_list(auth_user, session, **kwargs):
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

    query = kwargs['query_params']
    if 'id' in query:
        params['id'] = validate_list_int(query['id'])

    if 'text' in query:
        params['text'] = validate_string(query['text'])

    if 'is_online' in query and query['is_online']:
        params['is_online'] = query['is_online']

    if 'is_user' in query and query['is_user']:
        params['is_user'] = query['is_user']

    if 'limit' in query:
        params['limit'] = validate_mLimit(query['limit'])

    if 'topic' in query:
        params['topic'] = validate_string(query['topic'])

        if 'type' in query:
            if query['type'] in dict(TOPIC_TYPE):
                params['_type'] = query['type']

    new_param = {
        'user': auth_user,
        'session': session,
        'instance': Persons.get_persons_list(**params).all(),
    }

    if not params['topic'] is None:
        return mPersonRoleSerializer(**new_param).data

    return mPersonSerializer(**new_param).data
