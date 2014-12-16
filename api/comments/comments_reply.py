# coding: utf-8
from comments_create import post as create_comment
from utils import need_authorization
from utils.exceptions import RequestErrorException


@need_authorization
def post(parent_id, auth_user, session, **kwargs):
    if 'text' in kwargs['query_params']:
        text = kwargs['query_params']['text']
    else:
        raise RequestErrorException

    params = {
        'query_params': {
            'text': text,
            'parent_id': parent_id
        }
    }

    return create_comment(auth_user=auth_user, session=session, **params)
