# coding: utf-8

import zerorpc
import unittest
from zerorpc.exceptions import RemoteError

from utils.connection import create_session, db_connect, mongo_connect
from tests.create_test_user import create, clear
from tests.constants import ZERORPC_SERVICE_URI
from models.base import Base
from models.tokens import GlobalToken


def get_token_by_id(user_id, session):
    gt = session.query(GlobalToken).filter(GlobalToken.user_id == user_id)

    gta = [gte for gte in gt]
    assert len(gta) == 1

    return gta[0].token


def setUpModule():
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")
    Base.metadata.create_all(bind=engine)
    mongo_connect()


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
        Auth_IPC_pack = {
                    'api_method': '/auth/session',
                    'api_type': 'get',
                    'token': self.token,
                    'x_token': None,
                    'query_params': {}}

        auth_resp = self.cl.route(Auth_IPC_pack)

        session_token = auth_resp['x-token']
        
        IPC_pack = {
            'api_method': '/test/echoauth',
            'api_type': 'get',
            'x_token': session_token,
            'query_params': {'message': 'hello'}
        }
        resp = self.cl.route(IPC_pack)

        self.assertEqual({'message': "Hello,Test1"}, resp)

    def test_revoke(self):
        Auth_IPC_pack = {
            'api_method': '/auth/session',
            'api_type': 'get',
            'token': self.token,
            'x_token': None,
            'query_params': {}
        }
        auth_resp = self.cl.route(Auth_IPC_pack)

        session_token = auth_resp['x-token']
        Del_IPC_pack = {
            'api_method': '/auth/session',
            'api_type': 'delete',
            'x_token': session_token,
            'query_params': {},
            'token': None
        }
        auth_resp = self.cl.route(Del_IPC_pack)
        
        IPC_pack = {
            'api_method': '/test/echoauth',
            'api_type': 'get',
            'x_token': session_token,
            'query_params': {'message': 'hello'}
        }

        try:
            self.cl.route(IPC_pack)
        except RemoteError, re:
            self.assertEqual(re.name, "NotAuthorizedException")

    def tearDown(self):
        clear(self.session)
        self.cl.close()
