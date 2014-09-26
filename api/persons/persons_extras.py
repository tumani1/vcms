# coding: utf-8

from models.topics import Topics
from models.extras import ExtrasTopics, Extras
from models.extras.constants import APP_EXTRA_TYPE

from utils.validation import validate_mLimit, validate_list_int, validate_int

__all__ = ['get_person_extars']


def get_person_extars(person_id, auth_user, session, **kwargs):
    # Validation person value
    person_id = validate_int(person_id, min_value=1)

    # Params
    params = {
        'id': None,
        'text': None,
        '_type': None,
        'limit': None,
        'person': person_id,
        'session': session,
    }

    query = kwargs['query_params']
    if 'id' in query:
        params['id'] = validate_list_int(query['id'])

    if 'text' in query:
        params['text'] = str(query['text']).strip()

    if 'type' in query:
        if query['type'] in dict(APP_EXTRA_TYPE).keys():
            params['_type'] = query['type']

    if 'limit' in query:
        params['limit'] = validate_mLimit(limit=query['limit'])


    result = Extras.get_extras_by_person(**params).all()

    return Extras.data(result)

