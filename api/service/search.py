# coding: utf-8

from models import Persons, Topics, Media, MediaUnits

from utils.exceptions import RequestErrorException
from utils.validation import validate_mLimit, validate_string

__all__ = ['get_search_list']


def get_search_list(auth_user, session, **kwargs):
    # Params
    params = {
        'limit': None,
        'text': None,
        'session': session,
    }

    query = kwargs['query_params']

    if 'text' in query:
        params['text'] = validate_string(query['text'])

    if 'limit' in query:
        params['limit'] = 10

    text = params['text']
    if text is None:
        raise RequestErrorException(u'Empty text field')


    Persons.get_search_by_text(**params).all()
    Topics.get_search_by_text(**params).all()
    Media.get_search_by_text(**params).all()
    MediaUnits.get_search_by_text(**params).all()




    # query = PersonsValues.get_person_values(**params).all()
