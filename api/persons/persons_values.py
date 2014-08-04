# coding: utf-8

from models.persons import PersonsValues
from api.serializers import mValue

from utils.validation import validate_list_string, validate_int

__all__ = ['get_person_values']


def get_person_values(id, auth_user, session, **kwargs):
    # Validation person value
    person = validate_int(id, min_value=1)

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
        raise Exception(u"Empty name")

    if params['value'] is None:
        raise Exception(u"Empty value")

    query = PersonsValues.get_person_values(**params).all()

    return mValue(instance=query, session=session).data
