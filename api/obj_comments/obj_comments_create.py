# coding: utf-8
from api.comments.comments_create import post as create_comments


def post(type, id, auth_user, session, text, **kwargs):
    params = {
        'auth_user': auth_user,
        'session': session,
        'obj_type': type,
        'text': text
    }

    query = kwargs['query']
    if 'id' in query:
        params.update(obj_id=id)
        return create_comments(**params)

    elif 'name' in query:
        params.update(obj_name=query['name'])
        return create_comments(**params)
