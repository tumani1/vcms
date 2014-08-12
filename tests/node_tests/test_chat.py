# coding=utf-8
#TODO: Создание и очистка записей ужасная, обязательно переделывать


import unittest
import requests
from settings import NODE
from models import ChatMessages, Base
from utils.connection import mongo_connect, db_connect, create_session

from datetime import datetime, timedelta
from fixtures import create, create_chat, create_users_chat


HOST = NODE['rest_ws_serv']['host']
PORT = NODE['rest_ws_serv']['port']
URL = 'http://{}:{}'.format(HOST, PORT)


def setUpModule():
    engine = db_connect().connect()
    mongo_connect()
    # engine.execute("drop schema public cascade; create schema public;")
    session = create_session(bind=engine)

    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)
    create_chat(session)
    create_users_chat(session)


    engine.close()


def tearDownModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")


class ChatInfoTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()

    def test_get_info(self):
        resp = self.req_sess.get(self.fullpath + '/chat/1/info')
        resp = resp.json()
        self.assertEqual(resp['description'], u'chat for testing')

    def test_get_info_nonexistent(self):
        resp = self.req_sess.get(self.fullpath+'/chat/0/info')
        self.assertEqual(resp.status_code, 400)

    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()


class ChatStatTestCase(unittest.TestCase):


    def setUp(self):
        mongo_connect()
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'})
        self.gl_token = resp.json()['token']

    def test_get_stat(self):
        ChatMessages.objects.create(text='for stat', created=datetime.utcnow()+timedelta(1,0,0))
        resp = self.req_sess.get(self.fullpath+'/chat/1/stat', headers={'token': self.gl_token})
        resp = resp.json()
        self.assertEqual(resp['new_msgs'], 1)

    def test_get_stat_nonexistent(self):
        resp = self.req_sess.get(self.fullpath+'/chat/0/stat', headers={'token': self.gl_token})
        self.assertEqual(resp.status_code, 404)


    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()


class ChatStreamTestCase(unittest.TestCase):

    def setUp(self):
        mongo_connect()

        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()

        self.cm = ChatMessages.objects.create(text='test', chat_id=1)

    def test_get_stream(self):
        resp = self.req_sess.get(self.fullpath+'/chat/1/stream')
        resp = resp.json()
        self.assertEqual(len(resp), 1)

    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()


class ChatSendTestCase(unittest.TestCase):

    def setUp(self):
        mongo_connect()

        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'})
        self.gl_token = resp.json()['token']

    def test_chat_send(self):
        resp = self.req_sess.put(self.fullpath+'/chat/1/send', headers={'token': self.gl_token}, data={'text': 'for send'})
        stat = self.req_sess.get(URL+'/chat/1/stat', headers={'token': self.gl_token})
        stat = stat.json()
        self.assertEqual(stat['new_msgs'], 1)

    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()