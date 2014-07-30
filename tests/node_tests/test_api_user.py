# coding: utf-8

import unittest
from models import Base, Users, UsersValues
from sqlalchemy.orm import sessionmaker, scoped_session
from utils.connection import db_connect, create_session
from tests.fixtures import create, create_scheme, create_users_values, create_topic, create_users_rels
import random
from settings import NODE
import requests
import json


def setUpModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")
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


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)
        self.req_sess = requests.Session()
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.user_id = 1
        token_str = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'}).content
        self.token = json.loads(token_str)['token']

    def tearDown(self):
        self.session.close()

    def test_info_get(self):
        resp = self.req_sess.get(self.fullpath+'/user/info', headers={'token': self.token})
        temp = {
            u'city': u'Test',
            u'userpic': u'Test1',
            u'firstname': u'Test1',
            u'country': u'Test',
            u'time_zone': u'UTC',
            u'lastname': u'Test1',
            u'id': 1
        }
        self.assertDictEqual(resp.json(), temp)

    def test_info_put(self):
        data = {'firstname': 'Ivan', 'lastname': 'Ivanov'}
        resp = self.req_sess.put(self.fullpath+'/user/info', headers={'token': self.token}, data=data)
        test_user = self.session.query(Users).filter_by(id=self.user_id).first()
        self.assertEqual(test_user.firstname, data['firstname'])
        self.assertEqual(test_user.lastname, data['lastname'])

    def test_values_put(self):
        data = {'name': ['shm1', 'shm2'], 'topic': 'test1', 'value': [23, 'str']}
        resp = self.req_sess.put(self.fullpath+'/user/values', headers={'token': self.token}, data=data)
        user_val = self.session.query(UsersValues).all()
        self.assertEqual(user_val[0].value_int, data['value'][0])
        self.assertEqual(user_val[0].scheme_id, 1)
        self.assertEqual(user_val[1].value_string, data['value'][1])
        self.assertEqual(user_val[1].scheme_id, 2)

    def test_values_get(self):
        data = {'topic': 'test1'}
        resp = self.req_sess.get(self.fullpath+'/user/values', headers={'token': self.token}, params=data)
        temp = [{u'id': 1, u'value': 777}]
        self.assertListEqual(temp, resp.json())

    def test_friends_get(self):
        data = {'limit': '4'}
        resp = self.req_sess.get(self.fullpath+'/user/friends', headers={'token': self.token}, params=data)
        temp = [{u'lastname': u'Test2', u'relation': u'f', u'id': 2, u'firstname': u'Test2', u'is_online': False}]
        self.assertListEqual(resp.json(), temp)

    def test_password_put(self):
        old_pass = self.session.query(Users).filter_by(id=2).first().password
        data = {'password': 'testtest'+ str(random.randint(1,100))}
        token_str = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test2@test.ru', 'password': 'Test2'}).content
        self.token = json.loads(token_str)['token']
        resp = self.req_sess.put(self.fullpath+'/user/password', headers={'token': self.token}, data=data)
        self.session.close()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        new_pass = self.session.query(Users).filter_by(id=2).first().password
        self.assertNotEqual(old_pass, new_pass)
