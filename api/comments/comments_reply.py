# coding: utf-8
from comments_create import post as create_comment


def post(parent_id, auth_user, session, **kwargs):
    if 'text' in kwargs['query']:
        text = kwargs['query']['text']
    else:
        raise Exception(u"Empty name")

    params = {
        'query': {
            'text': text,
            'parent_id': parent_id
        }
    }

    return create_comment(auth_user, session, **params)
