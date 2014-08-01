# coding: utf-8

from models.topics import TopicsValues
from utils.validation import validate_list_string

__all__ = ['get_topic_values']


def get_topic_values(auth_user, session, name, **kwargs):
    # Params
    params = {
        'name': name,
        'session': session,
        'scheme_name': None,
    }

    if 'scheme_name' in kwargs:
        params['scheme_name'] = validate_list_string(kwargs['scheme_name'])

    if params['scheme_name'] is None:
        return {'code': 404}

    query = TopicsValues.get_values_through_schema(**params).all()

    return TopicsValues.data(query)
