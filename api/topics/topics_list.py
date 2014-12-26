# coding: utf-8

from models.topics import Topics
from models.topics.constants import TOPIC_TYPE

from api.serializers import mTopicSerializer

from utils.validation import validate_mLimit, validate_string

__all__ = ['get_topics_list']


def get_topics_list(auth_user, session, **kwargs):
    # Init Params
    params = {
        'user': auth_user,
        'session': session,
        'name': None,
        'text': None,
        '_type': None,
        'limit': None,
    }

    query = kwargs['query_params']
    if 'name' in query:
        params['name'] = validate_string(query['name'])

    if 'text' in query:
        params['text'] = validate_string(query['text'])

    if 'type' in query:
        if query['type'] in dict(TOPIC_TYPE):
            params['_type'] = query['type']

    if 'limit' in query:
        params['limit'] = validate_mLimit(limit=query['limit'])

    # Params
    params = {
        'user': auth_user,
        'session': session,
        'instance': Topics.get_topics_list(**params).all(),
    }

    return mTopicSerializer(**params).data
