# coding: utf-8

from models import db, PersonsValues
from utils.validation import validate_list_string

__all__ = ['get_person_values']


@db
def get_person_values(user, person, session, **kwargs):
    # Params
    params = {
        'person': person,
        'session': session,
        'name': None,
        'topic': None,
        'value': None,
    }

    if 'name' in kwargs:
        params['name'] = validate_list_string(kwargs['name'])

    if 'topic' in kwargs:
        try:
            params['topic'] = str(kwargs['topic']).strip()
        except Exception, e:
            pass

    if 'value' in kwargs:
        value = kwargs['value']
        if not isinstance(value, list):
            value = [value]

        clean_value = []
        for i in value:
            try:
                clean_value.append(int(i))
            except Exception, e:
                clean_value.append(str(i))

        if len(clean_value):
            params['value'] = clean_value


    if params['name'] is None:
        return {'code': 404}

    if params['value'] is None:
        return {'code': 404}

    query = PersonsValues.get_person_values(**params).all()

    return PersonsValues.data(query)
