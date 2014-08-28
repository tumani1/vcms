# coding: utf-8
import unittest
import requests
from datetime import datetime, timedelta

from models import ChatMessages, Base, Users, Chats
from utils.connection import mongo_connect, db_connect, create_session
from datetime import datetime, timedelta
from tests.fixtures import create, create_chat, create_users_chat
from tests.constants import NODE


HOST = NODE['rest_ws_serv']['host']
PORT = NODE['rest_ws_serv']['port']
URL = 'http://{}:{}'.format(HOST, PORT)


def setUpModule():
    engine = db_connect().connect()
    mongo_connect()
    ChatMessages.objects.delete()
    engine.execute("drop schema public cascade; create schema public;")
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
    engine.execute("drop schema public cascade; create schema public;")
    ChatMessages.objects.delete()


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
        ChatMessages.objects.delete()
        self.session.close()
        self.engine.close()
        self.req_sess.close()


class ChatStatTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)
        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)
        self.req_sess = requests.Session()
        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'})
        self.gl_token = resp.json()['token']

    def test_get_stat(self):
        ch = self.session.query(Chats).first()
        ChatMessages.objects.create(text='for stat', chat_id=ch.id, created=datetime.utcnow()+timedelta(1,0,0))
        resp = self.req_sess.get(self.fullpath+'/chat/{0}/stat'.format(ch.id), headers={'token': self.gl_token})
        resp = resp.json()
        self.assertEqual(resp['new_msgs'], 1)

    def test_get_stat_nonexistent(self):
        resp = self.req_sess.get(self.fullpath+'/chat/0/stat', headers={'token': self.gl_token})
        self.assertEqual(resp.status_code, 400)

    def tearDown(self):
        ChatMessages.objects.delete()
        self.session.close()
        self.engine.close()
        self.req_sess.close()


class ChatStreamTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)
        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)
        self.req_sess = requests.Session()
        self.u = self.session.query(Users).first()
        self.ch = self.session.query(Chats).first()
        self.cm = ChatMessages.objects.create(text='test', chat_id=1, user_id=self.u.id)

    def test_get_stream(self):
        resp = self.req_sess.get(self.fullpath+'/chat/{0}/stream'.format(self.ch.id))
        resp = resp.json()
        self.assertEqual(len(resp), 1)

    def tearDown(self):
        ChatMessages.objects.delete()
        self.session.close()
        self.engine.close()
        self.req_sess.close()


class ChatSendTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)
        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)
        self.req_sess = requests.Session()
        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'})
        self.gl_token = resp.json()['token']

    def test_chat_send(self):
        data={'text': 'for send'}
        ch = self.session.query(Chats).first()
        resp = self.req_sess.put(self.fullpath+'/chat/{0}/send'.format(ch.id),
                                 headers={'token': self.gl_token}, data=data)
        m = ChatMessages.objects.first()
        self.assertEqual(m.text, data['text'])

    def tearDown(self):
        ChatMessages.objects.delete()
        self.session.close()
        self.engine.close()
        self.req_sess.close()