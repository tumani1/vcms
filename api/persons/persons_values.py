# coding: utf-8

from models import db, PersonsValues

__all__ = ['get_person_values']


@db
def get_person_values(person, session, **kwargs):
    # Params
    params = {
        'person': person,
        'session': session,
        'name': None,
        'topic': None,
        'value': None,
    }

    if 'name' in kwargs:
        name = kwargs['name']
        if not isinstance(name, list):
            try:
                params['name'] = [str(name).strip()]
            except Exception, e:
                pass
        else:
            if isinstance(name, list):
                try:
                    params['name'] = [str(i).strip() for i in name]
                except Exception, e:
                    pass

    if 'topic' in kwargs:
        try:
            params['topic'] = str(kwargs['topic']).strip()
        except Exception, e:
            pass

    if 'value' in kwargs:
        value = kwargs['value']
        if not isinstance(value, list):
            try:
                params['value'] = [str(value).strip()]
            except Exception, e:
                pass
        else:
            if isinstance(value, list):
                try:
                    params['value'] = [str(i).strip() for i in value]
                except Exception, e:
                    pass

    if params['name'] is None:
        return {'code': 404}

    if params['value'] is None:
        return {'code': 404}

    query = PersonsValues.get_values_through_schema(**params).all()

    return PersonsValues.data(query)
