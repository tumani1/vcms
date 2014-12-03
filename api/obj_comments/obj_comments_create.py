# coding: utf-8
from api.comments.comments_create import post as create_comments
from utils import need_authorization
from utils.exceptions import RequestErrorException


@need_authorization
def post(type, comment, auth_user, session, query_params, **kwargs):
    id, name = None, None

    try:
        id = int(comment)
    except ValueError:
        name = comment

    if 'text' in query_params:
        text = query_params['text']
    else:
        raise RequestErrorException

    params = {
        'auth_user': auth_user,
        'session': session,
        'query_params': {'obj_type': type, 'text': text}
    }

    if id:
        params['query_params'].update(obj_id=id)
    elif name:
        params['query_params'].update(obj_name=name)

    return create_comments(**params)
