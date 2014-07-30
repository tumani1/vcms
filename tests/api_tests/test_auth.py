# coding: utf-8

import zerorpc
import unittest
from zerorpc.exceptions import RemoteError

from utils.connection import create_session, db_connect
from tests.create_test_user import create, clear
from models import GlobalToken
from tests.constants import ZERORPC_SERVICE_URI


def get_token_by_id(user_id, session):
    gt = session.query(GlobalToken).filter(GlobalToken.user_id == user_id)

    gta = [gte for gte in gt]
    assert len(gta) == 1

    return gta[0].token


class ZeroRpcServiceAuthTestCase(unittest.TestCase):

    user_id = None
    token = None
    session_token = None

    def setUp(self):
        self.cl = zerorpc.Client()
        self.cl.connect(ZERORPC_SERVICE_URI)
        
        
        self.session = create_session(bind=db_connect(), expire_on_commit=False)
        clear(self.session)
        variable = create(self.session)
        self.user = variable
        self.token = self.user.global_token.token

    def test_echo(self):
        Auth_IPC_pack = {'api_group': 'auth',
                    'api_method': 'session',
                    'http_method': 'get',
                    'token': self.token,
                    'x_token': None,
                    'query_params':{}}

        auth_resp = self.cl.route(Auth_IPC_pack)

        session_token = auth_resp['session_token']
        
        IPC_pack = {
            'api_group': 'test',
            'api_method': 'echo_auth',
            'http_method': 'get',
            'x_token': session_token,
            'query_params': {'message': 'hello'}
        }
        resp = self.cl.route(IPC_pack)

        print "Before assert \n", IPC_pack, '\n resp', resp
        self.assertEqual({'message': "Hello,Test"}, resp)

    def test_revoke(self):
        Auth_IPC_pack = {
            'api_group': 'auth',
            'api_method': 'session',
            'http_method': 'get',
            'token': self.token,
            'x_token': None,
            'query_params': {}
        }
        auth_resp = self.cl.route(Auth_IPC_pack)

        session_token = auth_resp['session_token']
        Del_IPC_pack = {
            'api_group': 'auth',
            'api_method': 'session',
            'http_method': 'delete',
            'x_token': session_token,
            'query_params': {},
            'token': None
        }
        auth_resp = self.cl.route(Del_IPC_pack)
        
        IPC_pack = {
            'api_group': 'test',
            'api_method': 'echo_auth',
            'http_method': 'get',
            'x_token': session_token,
            'query_params': {'message': 'hello'}
        }

        try:
            self.cl.route(IPC_pack)
        except RemoteError, re:
            self.assertEqual(re.name,  "NotAuthorizedException")

    def tearDown(self):
        clear(self.session)
        self.cl.close()
