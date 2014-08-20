# coding: utf-8

from models.users import Users
from models.tokens import SessionToken, GlobalToken

from api.users import routing as users_routing
from api.topics import routing as topics_routing
from api.persons import routing as persons_routing
from api.media_unit import routing as media_unit_routing
from api.test import routing as test_routing
from api.user import routing as user_routing
from api.auth import routing as auth_routing
from api.msgr import routing as msgr_routing
from api.media import routing as media_routing
from api.content import routing as content_routes
from api.stream import routing as stream_routes
from api.chat import routing as chat_routes
from api.comments import routing as comments_routing
from api.obj_comments import routing as obj_comments_routing
from api.cdn import routing as cdn_routing


rest_routes = {
    'mediaunits': media_unit_routing,
    'user': user_routing,
    'users': users_routing,
    'topics': topics_routing,
    'persons': persons_routing,
    'test': test_routing,
    'auth': auth_routing,
    'media': media_routing,
    'msgr': msgr_routing,    
    'content': content_routes,
    'stream': stream_routes,
    'chat': chat_routes,
    'comments': comments_routing,
    'obj_comments': obj_comments_routing,
}

internal_routes = {
    'int-api': cdn_routing,
}


def authorize(IPC_pack, session=None):
    user_id = None
    if 'x_token' in IPC_pack['query_params']:
        x_token = IPC_pack['query_params']['x_token']
        user_id = SessionToken.get_user_id_by_token(token_string=x_token, session=session)
    elif 'token' in IPC_pack['query_params']:
        token = IPC_pack['query_params']['token']
        user_id = GlobalToken.get_user_id_by_token(token_string=token, session=session)

    user = None
    if user_id:
        user = session.query(Users).get(user_id)

    return user
