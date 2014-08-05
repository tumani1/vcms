# coding: utf-8
from comments_create import post as create_comment


def post(id, auth_user, session, **kwargs):
    if 'text' in kwargs['query']:
        text = kwargs['query']['text']
    else:
        raise Exception(u"Empty name")
    params = {
        'query': {
            'text': text,
            'parent_id': id
        }
    }
    return create_comment(auth_user, session, **params)
