# coding: utf-8

from models.extras import Extras
from models.extras.constants import APP_EXTRA_TYPE

from utils.validation import validate_mLimit, validate_list_int

__all__ = ['get_topic_extars']


def get_topic_extars(name, auth_user,  session, **kwargs):
    # Params
    params = {
        'id': None,
        'text': None,
        '_type': None,
        'limit': None,
        'name': name,
        'session': session,
    }

    query = kwargs['query']
    if 'id' in query:
        params['id'] = validate_list_int(query['id'])

    if 'text' in query:
        try:
            params['text'] = str(kwargs['text']).strip()
        except:
            pass

    if 'type' in query:
        if query['type'] in dict(APP_EXTRA_TYPE).keys():
            params['_type'] = query['type']

    if 'limit' in query:
        params['limit'] = validate_mLimit(limit=query['limit'])

    result = Extras.get_extras_by_topics(**params).all()

    return Extras.data(result)
