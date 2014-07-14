# coding=utf-8
from models.content import Content
from serializer import mContentSerializer
from utils.validation import validate_list_int, validate_int, validate_string


class RequiredParams(Exception):
    pass


def get_content_list(auth_user, session, **kwargs):

    params = {}
    if 'id' in kwargs:
        params['id'] = validate_list_int(kwargs['id'])

    if 'obj_type' in kwargs:
        params['obj_type'] = validate_string(kwargs['obj_type'])

        keys = set(kwargs.keys())
        if not keys.intersection({'obj_id', 'obj_name'}):
            raise RequiredParams('request must contain obj_id or obj_name params')

        if 'obj_id' in kwargs:
            params['obj_id'] = validate_int(kwargs['obj_id'])

        if 'obj_name' in kwargs and 'obj_id' not in kwargs:
            params['obj_name'] = validate_string(kwargs['obj_name'])

    c_list = Content.get_content_list(session, **params)
    data = mContentSerializer(c_list).get_data()
    return data