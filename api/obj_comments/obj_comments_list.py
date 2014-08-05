# coding: utf-8
from api.comments.comments_list import get as get_comments_list


def get(auth_user, session, type, **kwargs):
    params = {
        'auth_user': auth_user,
        'session': session,
        'obj_type': type
    }

    query = kwargs['query']
    if 'id' in query:
        params.update(obj_id=query['id'])
        return get_comments_list(**params)

    elif 'name' in query:
        params.update(obj_name=query['name'])
        return get_comments_list(**params)
