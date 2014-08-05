# coding: utf-8
from api.comments.comments_create import post as create_comments


def post(type, name_or_id, auth_user, session, **kwargs):
    query = kwargs['query']
    id, name = None, None

    try:
        id = int(name_or_id)
    except ValueError:
        name = name_or_id

    if 'text' in query:
        text = query['text']
    else:
        raise Exception(u"Empty name")

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
