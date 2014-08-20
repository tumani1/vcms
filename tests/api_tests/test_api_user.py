# coding: utf-8

import random
import zerorpc
import unittest

from sqlalchemy.orm import sessionmaker, scoped_session

from models import Base, SessionToken, Users, UsersValues
from utils.connection import db_connect, create_session

from tests.constants import ZERORPC_SERVICE_URI
from tests.fixtures import create, create_scheme, create_users_values, create_topic, create_users_rels


def setUpModule():
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")
    session = create_session(bind=engine)
    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)
    create_users_rels(session)
    create_topic(session)
    create_scheme(session)
    create_users_values(session)



def tearDownModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")


class UsersTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.cl = zerorpc.Client(timeout=3000, heartbeat=100000)
        self.cl.connect(ZERORPC_SERVICE_URI, )
        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)

    def tearDown(self):
        self.cl.close()
        self.session.close()

    def test_info_get(self):
        IPC_pack = {
                    'api_method': '/user/info',
                    'api_type': 'get',
                    'query_params': {
                        'x_token': self.session_token[1]
                    }
        }
        temp = {
                'city': u'Test',
                'userpic': u'Test1',
                'firstname': u'Test1',
                'country': u'Russian Federation',
                'time_zone': u'UTC',
                'lastname': u'Test1',
                'id': 1
        }
        resp = self.cl.route(IPC_pack)
        self.assertDictEqual(resp, temp)

    def test_info_put(self):
        IPC_pack = {
                    'api_method': '/user/info',
                    'api_type': 'put',
                    'query_params': {
                        'firstname': 'Ivan',
                        'lastname': 'Ivanov',
                        'x_token': self.session_token[1]}
        }
        resp = self.cl.route(IPC_pack)
        test_user = self.session.query(Users).filter_by(id=self.user_id).first()
        self.assertEqual(test_user.firstname, IPC_pack['query_params']['firstname'])
        self.assertEqual(test_user.lastname, IPC_pack['query_params']['lastname'])

    def test_values_put(self):
        IPC_pack = {
                    'api_method': '/user/values',
                    'api_type': 'put',
                    'x_token': self.session_token[1],
                    'query_params': {'name': ['shm1', 'shm2'], 'topic': 'test1', 'value': [23, 'str']}
        }
        resp = self.cl.route(IPC_pack)
        user_val = self.session.query(UsersValues).all()
        self.assertEqual(user_val[0].value_int, IPC_pack['query_params']['value'][0])
        self.assertEqual(user_val[0].scheme_id, 1)
        self.assertEqual(user_val[1].value_string, IPC_pack['query_params']['value'][1])
        self.assertEqual(user_val[1].scheme_id, 2)

    def test_values_get(self):
        IPC_pack = {
                    'api_method': '/user/values',
                    'api_type': 'get',
                    'x_token': self.session_token[1],
                    'query_params': {'topic': 'test1'}
        }
        resp = self.cl.route(IPC_pack)
        temp = {'name': 1, 'value': 777}
        self.assertDictEqual(temp, resp[0])

    def test_friends_get(self):
        IPC_pack = {
                    'api_method': '/user/friends',
                    'api_type': 'get',
                    'x_token': self.session_token[1],
                    'query_params': {'limit': '4'}
        }
        resp = self.cl.route(IPC_pack)
        temp = {'lastname': 'Test2', 'relation': 'f', 'id': 2, 'firstname': 'Test2', 'is_online': False}
        self.assertDictEqual(resp[0], temp)

    def test_password_put(self):
        IPC_pack = {
                    'api_method': '/user/password',
                    'api_type': 'put',
                    'x_token': self.session_token[1],
                    'query_params': {'password': 'testtest'+ str(random.randint(1,100))}
        }
        old_pass = self.session.query(Users).filter_by(id=self.user_id).first().password
        resp = self.cl.route(IPC_pack)
        self.session.close()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        new_pass = self.session.query(Users).filter_by(id=self.user_id).first().password
        self.assertNotEqual(old_pass, new_pass)
