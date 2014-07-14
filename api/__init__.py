# coding: utf-8

from models import Users

from api.users import routing as users_routing
from api.topics import routing as topics_routing
from api.persons import routing as persons_routing
from api.media_unit import routing as media_unit_routing
from api.test import routes as test_routing
from api.user import routing as user_routing
from api.auth import auth
from api.msgr import routing as msgr_routing
from api.media import routing as media_routing
from api.content import routing as content_routes
from api.stream import routing as stream_routes
from api.chat import routing as chat_routes
from api.comments import routing as comments_routing
from models import SessionToken, GlobalToken


routes = {
    'mediaunits': media_unit_routing,
    'user': user_routing,
    'users': users_routing,
    'topics': topics_routing,
    'persons': persons_routing,
    'test': test_routing,
    'auth': auth,
    'media': media_routing,
    'msgr': msgr_routing,    
    'content': content_routes,
    'stream': stream_routes,
    'chat': chat_routes,
    'comments': comments_routing
}


def authorize(IPC_pack, session=None):
    user = session.query(Users).get(1)
    IPC_pack['query_params'].update({'auth_user': user})
    # if IPC_pack['api_group'] == 'auth':
    #     IPC_pack['query_params'].update({
    #         'x_token': IPC_pack['x_token'] if 'x_token' in IPC_pack else None,
    #         'token': IPC_pack['token'],
    #     })
    #
    # user_id = None
    # if 'x_token' in IPC_pack and IPC_pack['x_token']:
    #     user_id = SessionToken.get_user_id_by_token(token_string=IPC_pack['x_token'], session=session)
    # elif 'token' in IPC_pack and IPC_pack['token']:
    #     user_id = GlobalToken.get_user_id_by_token(token_string=IPC_pack['token'], session=session)
    # user = None
    # if user_id:
    #     user = session.query(Users).get(user_id)
    #
    # IPC_pack['query_params'].update({'auth_user': user})

    return IPC_pack
