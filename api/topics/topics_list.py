# coding: utf-8

from models import dbWrap, Topics
from models.topics.constants import TOPIC_TYPE

__all__ = ['get_topics_list']


@dbWrap
def get_topics_list(user, session, **kwargs):
    # Params
    params = {
        'user': user,
        'session': session,
        'name': None,
        'text': None,
        '_type': None,
        'limit': None,
    }

    if 'name' in kwargs:
        try:
            params['name'] = str(kwargs['name'])
        except Exception, e:
            pass

    if 'text' in kwargs:
        try:
            params['text'] = str(kwargs['text'])
        except Exception, e:
            pass

    if 'type' in kwargs:
        if kwargs['type'] in dict(TOPIC_TYPE).keys():
            params['_type'] = kwargs['type']

    if 'limit' in kwargs:
        result = kwargs['limit'].split(',', 1)

        if len(result) == 1:
            params['limit'] = (result[0], 0)
        elif len(result) == 2:
            # Check limit
            if not len(result[0]):
                r1 = None
            else:
                try:
                    r1 = int(result[0])
                except Exception, e:
                    r1 = None

            # Check top
            try:
                r2 = int(result[1])
            except Exception, e:
                r2 = 0

            params['limit'] = (r1, r2)

    query = Topics.get_topics_list(**params)

    return Topics.data(user, query)
