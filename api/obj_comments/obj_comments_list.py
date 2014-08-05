# coding: utf-8
from api.comments.comments_list import get as get_comments_list


def get(type, name_or_id, auth_user, session,  **kwargs):
    id, name = None, None
    try:
        id = int(name_or_id)
    except ValueError:
        name = name_or_id
    params = {
        'auth_user': auth_user,
        'session': session,
        'query': {'obj_type': type}
    }

    if id:
        params['query'].update(obj_id=id)
        return get_comments_list(**params)

    elif name:
        params['query'].update(obj_name=name)
        return get_comments_list(**params)
