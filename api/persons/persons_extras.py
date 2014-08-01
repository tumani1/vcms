# coding: utf-8

from models.topics import Topics
from models.extras import ExtrasTopics, Extras
from models.extras.constants import APP_EXTRA_TYPE

from utils.validation import validate_mLimit, validate_list_int, validate_int

__all__ = ['get_person_extars']


def get_person_extars(auth_user, id, session, **kwargs):
    # Validation person value
    person = validate_int(id, min_value=1)

    # Params
    params = {
        'id': None,
        'text': None,
        '_type': None,
        'limit': None,
        'person': person,
        'session': session,
    }

    if 'id' in kwargs:
        params['id'] = validate_list_int(kwargs['id'])

    if 'text' in kwargs:
        params['text'] = str(kwargs['text']).strip()

    if 'type' in kwargs:
        if kwargs['type'] in dict(APP_EXTRA_TYPE).keys():
            params['_type'] = kwargs['type']

    if 'limit' in kwargs:
        params['limit'] = validate_mLimit(limit=kwargs['limit'])


    result = Extras.get_extras_by_person(**params).all()

    return Extras.data(result)

