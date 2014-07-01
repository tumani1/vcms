# coding: utf-8

from models import Extras
from models.extras.constants import APP_EXTRA_TYPE

from utils.validation import validate_mLimit, validate_list_int

__all__ = ['get_topic_extars']


def get_topic_extars(auth_user, name,  session, **kwargs):
    # Params
    params = {
        'id': None,
        'text': None,
        '_type': None,
        'limit': None,
        'name': name,
        'session': session,
    }

    if 'id' in kwargs:
        params['id'] = validate_list_int(kwargs['id'])

    if 'text' in kwargs:
        try:
            params['text'] = str(kwargs['text']).strip()
        except:
            pass

    if 'type' in kwargs:
        if kwargs['type'] in dict(APP_EXTRA_TYPE).keys():
            params['_type'] = kwargs['type']

    if 'limit' in kwargs:
        params['limit'] = validate_mLimit(limit=kwargs['limit'])

    result = Extras.get_extras_by_topics(**params).all()

    return Extras.data(result)
