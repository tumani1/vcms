# coding=utf-8

from models.content import Content
from api.serializers import mContentSerializer
from utils.exceptions import RequestErrorException
from utils.validation import validate_list_int, validate_int, validate_string


def get_content_list(auth_user, session, **kwargs):

    params = {}
    query = kwargs['query_params']
    if 'id' in query:
        params['id'] = validate_list_int(query['id'])

    if 'obj_type' in query:
        params['obj_type'] = validate_string(query['obj_type'])

        keys = set(query.keys())
        if not keys.intersection({'obj_id', 'obj_name'}):
            raise RequestErrorException

        if 'obj_id' in query:
            params['obj_id'] = validate_int(query['obj_id'])

        if 'obj_name' in query and 'obj_id' not in query:
            params['obj_name'] = validate_string(query['obj_name'])

    c_list = Content.get_content_list(session, **params)
    data = mContentSerializer(c_list).get_data()
    return data
