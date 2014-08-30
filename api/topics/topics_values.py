# coding: utf-8

from models.topics import TopicsValues
from api.serializers import mValue
from utils.exceptions import RequestErrorException
from utils.validation import validate_list_string

__all__ = ['get_topic_values']


def get_topic_values(name, auth_user, session, **kwargs):
    # Params
    params = {
        'name': name,
        'session': session,
        'scheme_name': None,
    }

    query = kwargs['query_params']
    if 'scheme_name' in query:
        params['scheme_name'] = validate_list_string(query['scheme_name'])

    if params['scheme_name'] is None:
        raise RequestErrorException

    query = TopicsValues.get_values_through_schema(**params).all()

    return mValue(instance=query, session=session).data
