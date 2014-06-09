# coding: utf-8

from models import db, Topics, ExtrasTopics, Extras
from models.extras.constants import EXTRA_TYPE

from utils.validation import validate_mLimit, validate_list_int

__all__ = ['get_person_extars']


@db
def get_person_extars(user, person, session, **kwargs):
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
        try:
            params['text'] = str(kwargs['text']).strip()
        except:
            pass

    if 'type' in kwargs:
        if kwargs['type'] in dict(EXTRA_TYPE).keys():
            params['_type'] = kwargs['type']

    if 'limit' in kwargs:
        params['limit'] = validate_mLimit(limit=kwargs['limit'])


    result = Extras.get_extras_by_person(**params).all()

    return Extras.data(result)

