# coding: utf-8
from api.comments.comments_create import post as create_comments


def post(auth_user, session, type, text, **kwargs):
    params = {
        'auth_user': auth_user,
        'session': session,
        'obj_type': type,
        'text': text
    }
    if 'id' in kwargs:
        params.update(obj_id=kwargs['id'])
        return create_comments(**params)
    elif 'name' in kwargs:
        params.update(obj_name=kwargs['name'])
        return create_comments(**params)
