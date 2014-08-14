# coding: utf-8
from api.comments.comments_list import get as get_comments_list


def get(type, comment, auth_user, session,  **kwargs):
    id, name = None, None
    try:
        id = int(comment)
    except ValueError:
        name = comment

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
