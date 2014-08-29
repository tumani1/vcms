# coding: utf-8
import unittest
import zerorpc

from models.base import Base
from models.tokens import SessionToken
from models.users import Users
from tests.constants import INTERNAL_ZERORPC_SERVICE_URI
from tests.fixtures import create
from utils.connection import get_session, create_session, db_connect
from utils.common import datetime_to_unixtime


def setUpModule():
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")
    session = create_session(bind=engine)
    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)
    session.close()


def tearDownModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")


class AuthApiTestCase(unittest.TestCase):
    def setUp(self):
        self.session = get_session()
        self.zero_client = zerorpc.Client(timeout=3000, heartbeat=100000)
        self.zero_client.connect(INTERNAL_ZERORPC_SERVICE_URI)
        self.user_id = 1
        self.ipc_pack = {
            'api_method': '/internal/{0}',
            'api_type': 'get',
            'x_token': None,
            'query_params': {}
        }

    def test_is_auth_true(self):
        self.ipc_pack['api_method'] = self.ipc_pack['api_method'].format("auth/check")
        self.ipc_pack['x_token'] = SessionToken.generate_token(self.user_id, self.session)[1]
        resp = self.zero_client.route(self.ipc_pack)
        self.assertTrue(resp)

    def test_is_auth_false(self):
        self.ipc_pack['api_method'] = self.ipc_pack['api_method'].format("auth/check")
        resp = self.zero_client.route(self.ipc_pack)
        self.assertFalse(resp)

    def test_get_auth_user(self):
        self.ipc_pack['api_method'] = self.ipc_pack['api_method'].format("info/user")
        self.ipc_pack['x_token'] = SessionToken.generate_token(self.user_id, self.session)[1]
        resp = self.zero_client.route(self.ipc_pack)
        user = self.session.query(Users).get(self.user_id)
        m_user_dict = {
            'id': user.id,
            'firstname': user.firstname.decode("utf-8"),
            'lastname': user.lastname.decode("utf-8"),
            'gender': user.gender.code.decode("utf-8"),
            'regdate': datetime_to_unixtime(user.created),
            'lastvisit': '',
            'is_online': True,
            'city': user.city.name.decode("utf-8"),
            'country': user.city.country.name.decode("utf-8"),
        }
        self.assertDictEqual(resp, m_user_dict)

    def test_get_session(self):
        self.ipc_pack['api_method'] = self.ipc_pack['api_method'].format("info/session")
        id_, token, date = SessionToken.generate_token(self.user_id, self.session)
        session = self.session.query(SessionToken).get(id_)
        self.ipc_pack['x_token'] = token
        resp = self.zero_client.route(self.ipc_pack)
        m_session_dict = {
            'id': id_,
            'user_id': session.user_id,
            'token': token,
            'created': datetime_to_unixtime(date),
            'is_active': True,
            'os': session.os,
            'browser': session.browser,
            'ip_address': session.ip_address,
            'device': session.device,
        }

        self.assertDictEqual(resp, m_session_dict)

    def tearDown(self):
        self.session.close()
        self.zero_client.close()


class CdnApiTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def on_play_auth_user(self):
        pass

    def on_play_without_auth_user(self):
        pass

    def on_update_auth_user(self):
        pass

    def on_update_without_auth_user(self):
        pass

    def on_done_auth_user(self):
        pass

    def on_done_without_auth_user(self):
        pass
