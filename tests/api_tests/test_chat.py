# coding=utf-8
#TODO: Создание и очистка записей ужасная, обязательно переделывать


import unittest
import requests
from settings import NODE
from models import Chats, ChatMessages, UsersChat
from utils.connection import get_session, mongo_connect
from tests.create_test_user import create, clear
from models import GlobalToken
from datetime import datetime, timedelta


HOST = NODE['rest_ws_serv']['host']
PORT = NODE['rest_ws_serv']['port']
URL = 'http://{}:{}'.format(HOST, PORT)


class ChatInfoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = get_session()
        cls.session.execute('ALTER SEQUENCE chats_id_seq RESTART WITH 1;')
        cls.c = Chats(description='chat for testing')
        cls.session.add(cls.c)
        cls.session.commit()

    def test_get_info(self):
        resp = requests.get(URL+'/chat/1/info')
        resp = resp.json()
        self.assertEqual(resp['description'], 'chat for testing')

    def test_get_info_nonexistent(self):
        resp = requests.get(URL+'/chat/0/info')
        resp = resp.json()
        self.assertNotIn('description', resp)

    @classmethod
    def tearDownClass(cls):
        clear(cls.session)
        cls.session.query(Chats).delete()
        cls.session.commit()
        cls.session.close()


class ChatStatTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mongo_connect()
        cls.session = get_session()
        cls.session.execute('ALTER SEQUENCE chats_id_seq RESTART WITH 1;')
        cls.session.execute('ALTER SEQUENCE users_id_seq RESTART WITH 1;')
        clear(cls.session)
        cls.c = Chats(description='chat for testing')
        cls.u = create(cls.session)
        cls.gt = cls.session.query(GlobalToken).filter_by(user_id=cls.u.id).one()
        cls.session.add(cls.c)
        cls.session.commit()
        cls.uc = UsersChat(user_id=cls.u.id, chat_id=cls.c.id, cuStatus='1')
        cls.session.add(cls.uc)
        cls.session.commit()

    def test_get_stat(self):
        ChatMessages.objects.create(text='for stat', created=datetime.utcnow()+timedelta(1,0,0))
        resp = requests.get(URL+'/chat/1/stat', headers={'token': ChatStatTestCase.gt.token})
        resp = resp.json()
        self.assertEqual(resp['new_msgs'], 1)

    def test_get_stat_nonexistent(self):
        resp = requests.get(URL+'/chat/0/stat', headers={'token': ChatStatTestCase.gt.token})
        resp = resp.json()
        self.assertNotIn('users_cnt', resp)

    @classmethod
    def tearDownClass(cls):
        ChatMessages.objects.delete()
        clear(cls.session)
        cls.session.query(Chats).delete()
        cls.session.commit()
        cls.session.close()


class ChatStreamTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mongo_connect()
        cls.session = get_session()
        cls.session.execute('ALTER SEQUENCE chats_id_seq RESTART WITH 1;')
        cls.c = Chats(description='chat for testing')
        cls.session.add(cls.c)
        cls.session.commit()
        cls.cm = ChatMessages.objects.create(text='test', chat_id=cls.c.id)

    def test_get_stream(self):
        resp = requests.get(URL+'/chat/1/stream')
        resp = resp.json()
        self.assertEqual(len(resp), 1)

    @classmethod
    def tearDownClass(cls):
        clear(cls.session)
        cls.session.query(Chats).delete()
        cls.session.commit()
        cls.session.close()
        ChatMessages.objects.delete()


class ChatSendTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mongo_connect()
        ChatMessages.objects.delete()
        cls.session = get_session()
        cls.session.execute('ALTER SEQUENCE chats_id_seq RESTART WITH 1;')
        cls.c = Chats(description='chat for testing')
        cls.u = create(cls.session)
        cls.gt = cls.session.query(GlobalToken).filter_by(user_id=cls.u.id).one()
        cls.session.add(cls.c)
        cls.session.commit()

    def test_chat_send(self):
        resp = requests.put(URL+'/chat/1/send', headers={'token': ChatSendTestCase.gt.token}, data={'text': 'for send'})
        stat = requests.get(URL+'/chat/1/stat', headers={'token': ChatSendTestCase.gt.token})
        stat = stat.json()
        self.assertEqual(stat['new_msgs'], 1)

    @classmethod
    def tearDownClass(cls):
        ChatMessages.objects.delete()
        clear(cls.session)
        cls.session.query(Chats).delete()
        cls.session.commit()
        cls.session.close()