from api.comments.comments_list import get as get_comments
from api.comments.comments_create import post as add_comments
from utils.constants import OBJECT_TYPE_NEWS
from utils.exceptions import RequestErrorException
from utils.validation import validate_string


def get(news_id, auth_user, session=None, **kwargs):
    params = {'query_params': {'obj_id': news_id, 'obj_type': OBJECT_TYPE_NEWS}}
    return get_comments(auth_user, session, **params)


def post(news_id, auth_user, session=None, **kwargs):

    if 'text' in kwargs['query_params']:
        text = validate_string(kwargs['query_params']['text'])
    else:
        raise RequestErrorException

    params = {'query_params': {'obj_id': news_id, 'obj_type': OBJECT_TYPE_NEWS, 'text': text}}
    return add_comments(session=session, auth_user=auth_user, **params)
