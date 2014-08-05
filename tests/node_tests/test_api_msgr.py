# coding: utf-8

import unittest

import requests
from websocket import create_connection

from models import Base, MsgrLog
from utils.connection import db_connect, create_session
from tests.fixtures import create, create_msgr_threads, create_users_msgr_threads, create_msgr_log
from settings import NODE


def setUpModule():

    engine = db_connect()
    #engine.execute("drop schema public cascade; create schema public;")
    session = create_session(bind=engine)
    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)
    create_msgr_threads(session)
    create_users_msgr_threads(session)
    create_msgr_log(session)


def tearDownModule():
    engine = db_connect()
    #engine.execute("drop schema public cascade; create schema public;")


class MsgrTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()
        self.ws = create_connection('ws://{}:{}'.format(self.h, self.p))

        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'})
        self.token = resp.json()['token']

    def tearDown(self):
        self.ws.close()
        self.req_sess.close()
        self.session.close()

    def test_stream_get(self):
        data = {
            'id': 1
        }
        resp = self.req_sess.get(self.fullpath+'/msgr/stream', headers={'token': self.token}, params=data)
        result = {
            u'thread': 1,
            u'created': u'2014-01-01',
            u'text': u'text',
            u'attach': None,
            u'user': {
                u'lastname': u'Test1',
                u'relation': u'u',
                u'id': 1,
                u'firstname': u'Test1',
                u'is_online': False
            },
            u'id': 1
        }
        self.assertDictEqual(resp.json()[0], result)

    def test_stat_get(self):
        resp = self.req_sess.get(self.fullpath+'/msgr/stat', headers={'token': self.token})
        param = {'new_msgs': 1}
        self.assertDictEqual(resp.json(), param)

    def test_create_put(self):
        data = {
            'user_ids': [1, 2],
            'text': 'test'
        }
        resp = self.req_sess.put(self.fullpath+'/msgr/create', headers={'token': self.token}, data=data)
        result = {
            u'msgr_cnt': 1,
            u'id': 2,
            u'users': [{
                u'lastname': u'Test1',
                u'id': 1,
                u'firstname': u'Test1',
                u'is_online': False,
                u'relation': u'u'
            },
            {
                u'lastname': u'Test2',
                u'id': 2,
                u'firstname': u'Test2',
                u'is_online': False,
                u'relation': u'u'
            }]
        }
        self.assertDictEqual(resp.json(), result)

    def test_list_get(self):
        result = {
            u'msgr_cnt': 2,
            u'id': 1,
            u'users': {
                u'lastname': u'Test1',
                u'id': 1,
                u'firstname': u'Test1',
                u'is_online': False,
                u'relation': u'u'
            }
        }
        resp = self.req_sess.get(self.fullpath+'/msgr/list', headers={'token': self.token})
        self.assertListEqual(resp.json(), [result])

    def test_send_put(self):
        data = {
            u'text': u'Hi',
            u'id': 1
        }
        resp = self.req_sess.put(self.fullpath+'/msgr/send', headers={'token': self.token}, data=data)
        msgr_log = MsgrLog.get_msgr_log_by_msgr_thread_id_and_user_id(self.session, 1, 1).all()
        self.assertEqual(data['text'], msgr_log[1].text)

