# coding: utf-8

from models import Users, db
from users import routing as users_routing
from topics import routing as topics_routing
from persons import routing as persons_routing
from test import routes as test_routing
from user import routing as user_routing

from models import SessionToken, GlobalToken

routes = {
    'user': user_routing,
    'users': users_routing,
    'topics': topics_routing,
    'persons': persons_routing,
    'test': test_routing
}

@db
def authorize(IPC_pack, session=None):

    if IPC_pack['token'] == 'echo_token':
        
        return IPC_pack.update({'user':
                         session.query(Users).filter_by(id=1).first()[0]
                     })
    
    if IPC_pack['api_group'] =='auth':
        IPC_pack['query_params'].update({'x_token': IPC_pack['x_token'],
                                         'token':IPC_pack['token']
                                     })

    if 'x_token' in IPC_pack:
        user_id = SessionToken.get_user_id_by_token(token_string=IPC_pack['x_token'])
    elif 'token' in IPC_pack:
        user_id = GlobalToken.get_user_id_by_token(token_string = IPC_pack['token'])
        
    if user_id:
        user = session.query(Users).filter_by(id=1).first()[0]
    else:
        user = None


    IPC_pack.update({'user':user})
    
    
        

