# coding: utf-8

from models.persons import PersonsValues
from api.serializers import mValue
from utils.exceptions import RequestErrorException

from utils.validation import validate_list_string, validate_int

__all__ = ['get_person_values']


def get_person_values(person_id, auth_user, session, **kwargs):
    # Validation person value
    person_id = validate_int(person_id, min_value=1)

    # Params
    params = {
        'person': person_id,
        'session': session,
        'name': None,
        'topic': None,
        'value': None,
    }

    query = kwargs['query']
    if 'name' in query:
        params['name'] = validate_list_string(query['name'])

    if 'topic' in query:
        try:
            params['topic'] = str(query['topic']).strip()
        except Exception, e:
            pass

    if 'value' in query:
        value = query['value']
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
        raise RequestErrorException

    if params['value'] is None:
        raise RequestErrorException

    query = PersonsValues.get_person_values(**params).all()

    return mValue(instance=query, session=session).data
