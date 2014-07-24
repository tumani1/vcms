# coding: utf-8
from api.comments.comments_list import get as get_comments_list


def get(auth_user, session, type, **kwargs):
    params = {
        'auth_user': auth_user,
        'session': session,
        'obj_type': type
    }
    if 'id' in kwargs:
        params.update(obj_id=kwargs['id'])
        return get_comments_list(**params)
    elif 'name' in kwargs:
        params.update(obj_name=kwargs['name'])
        return get_comments_list(**params)