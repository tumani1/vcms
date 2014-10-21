# coding: utf-8
import unittest
import zerorpc

from tests.constants import ZERORPC_SERVICE_URI
from models.tokens import SessionToken
from models.base import Base
from models.users import Users
from utils.common import datetime_to_unixtime, get_or_create
from utils.connection import db_connect, mongo_connect, get_session


def setUpModule():
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")
    Base.metadata.create_all(bind=engine)
    mongo_connect()


class InternalApiTestCase(unittest.TestCase):

    def setUp(self):
        self.session = get_session()
        self.client = zerorpc.Client(timeout=3000)
        self.client.connect(ZERORPC_SERVICE_URI)

        self.auth_user, create = get_or_create(session=self.session, model=Users,
                                               filter={'firstname': 'Test1', 'lastname': 'Test1'},
                                               create={'firstname': 'Test1', 'lastname': 'Test1', 'password': 'Test', 'email': 'test1@test.ru'})
        if create:
            self.session.commit()
        session_token = SessionToken.generate_token(user_id=self.auth_user.id, session=self.session)
        self.session_token = self.session.query(SessionToken).get(session_token[0])
        self.ipc_pack = {
            'api_method': '',
            'api_type': 'get',
            'x_token': session_token[1],
            'query_params': {}
        }

    def test_get_session(self):
        self.ipc_pack['api_method'] = "/int-api/info/session"
        self.ipc_pack['query_params'] = {
            'token': self.session_token.token
        }
        response = self.client.route(self.ipc_pack)
        m_session = {
            'id': self.session_token.id,
            'user_id': self.session_token.user_id,
            'token': self.session_token.token,
            'created': datetime_to_unixtime(self.session_token.created),
            'is_active': self.session_token.is_active,
            'os': None,
            'browser': None,
            'ip_address': None,
            'device': None,
        }
        self.assertDictEqual(m_session, response)

    def test_get_auth_user(self):
        self.ipc_pack['api_method'] = "/int-api/info/user"
        response = self.client.route(self.ipc_pack)
        m_user = {
            'city': None,
            'country': None,
            'firstname': self.auth_user.firstname,
            'lastname': self.auth_user.lastname,
            'gender': self.auth_user.gender.code,
            'id': self.auth_user.id,
            'is_online': True,
            'lastvisit': '',
            'regdate': datetime_to_unixtime(self.auth_user.created),
        }
        self.assertDictEqual(m_user, response)

    def test_is_auth_true(self):
        self.ipc_pack['api_method'] = "/int-api/auth/check"
        response = self.client.route(self.ipc_pack)
        self.assertTrue(response)

    def test_is_auth_false(self):
        self.ipc_pack['api_method'] = "/int-api/auth/check"
        self.ipc_pack['x_token'] = ''
        response = self.client.route(self.ipc_pack)
        self.assertFalse(response)