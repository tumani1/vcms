# coding: utf-8

from models import Topics
from db_engine import db
from models.topics.constants import TOPIC_TYPE

from serializer import mTopicSerializer

from utils.validation import validate_mLimit

__all__ = ['get_topics_list']


@db
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

    if 'name' in kwargs:
        try:
            params['name'] = str(kwargs['name']).strip()
        except Exception, e:
            pass

    if 'text' in kwargs:
        try:
            params['text'] = str(kwargs['text']).strip()
        except Exception, e:
            pass

    if 'type' in kwargs:
        if kwargs['type'] in dict(TOPIC_TYPE).keys():
            params['_type'] = kwargs['type']

    if 'limit' in kwargs:
        params['limit'] = validate_mLimit(limit=kwargs['limit'])

    instance = Topics.get_topics_list(**params).all()

    # Params
    params = {
        'user': auth_user,
        'instance': instance,
        'session': session,
    }

    return mTopicSerializer(**params).data
