# coding: utf-8

from models.topics import Topics
from models.topics.constants import TOPIC_TYPE

from api.serializers import mTopicSerializer

from utils.validation import validate_mLimit

__all__ = ['get_topics_list']


def get_topics_list(auth_user, session, **kwargs):
    # Params
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
        params['name'] = str(query['name']).strip()

    if 'text' in query:
        try:
            params['text'] = str(query['text']).strip()
        except Exception, e:
            pass

    if 'type' in query:
        if query['type'] in dict(TOPIC_TYPE).keys():
            params['_type'] = query['type']

    if 'limit' in query:
        params['limit'] = validate_mLimit(limit=query['limit'])

    # Params
    params = {
        'user': auth_user,
        'instance': Topics.get_topics_list(**params).all(),
        'session': session,
    }

    return mTopicSerializer(**params).data
