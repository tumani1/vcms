# coding: utf-8

from models import Users
from db_engine import db
from api.users import routing as users_routing
from api.topics import routing as topics_routing
from api.persons import routing as persons_routing
from api.media_unit import routing as media_unit_routing
from api.test import routes as test_routing
from api.user import routing as user_routing
from api.auth import auth

from models import SessionToken, GlobalToken


routes = {
    'mediaunits': media_unit_routing,
    'user': user_routing,
    'users': users_routing,
    'topics': topics_routing,
    'persons': persons_routing,
    'test': test_routing,
    'auth': auth
}


@db
def authorize(IPC_pack, session=None):
    if IPC_pack['api_group'] == 'auth':
        IPC_pack['query_params'].update({
            'x_token': IPC_pack['x_token'] if 'x_token' in IPC_pack else None,
            'token': IPC_pack['token'],
        })

    user_id = None
    if 'x_token' in IPC_pack and IPC_pack['x_token']:
        user_id = SessionToken.get_user_id_by_token(token_string=IPC_pack['x_token'], session=session)
    elif 'token' in IPC_pack and IPC_pack['token']:
        user_id = GlobalToken.get_user_id_by_token(token_string=IPC_pack['token'], session=session)

    user = None
    if user_id:
        user = session.query(Users).filter_by(id=user_id).first()

    IPC_pack['query_params'].update({'auth_user': user})

    return IPC_pack
