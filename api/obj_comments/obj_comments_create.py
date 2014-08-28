# coding: utf-8
from api.comments.comments_create import post as create_comments
from utils.exceptions import RequestErrorException


def post(type, comment, auth_user, session, **kwargs):
    query = kwargs['query']
    id, name = None, None

    try:
        id = int(comment)
    except ValueError:
        name = comment

    if 'text' in query:
        text = query['text']
    else:
        raise RequestErrorException

    params = {
        'auth_user': auth_user,
        'session': session,
        'query': {'obj_type': type, 'text': text}
    }

    if id:
        params['query'].update(obj_id=id)
        return create_comments(**params)

    elif name:
        params['query'].update(obj_name=name)
        return create_comments(**params)
