# coding: utf-8
import unittest
import requests
from websocket import create_connection

from models import Base, MsgrLog, SessionToken
from utils.connection import db_connect, create_session
from tests.fixtures import create, create_msgr_threads, create_users_msgr_threads, create_msgr_log
from tests.constants import NODE


def setUpModule():

    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")
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

        self.token = SessionToken.generate_token(self.user_id, session=self.session)[1]

    def tearDown(self):
        self.ws.close()
        self.req_sess.close()
        self.session.close()

    def test_stream_get(self):
        data = {
        }
        id = 1
        resp = self.req_sess.get(self.fullpath+'/msgr/{0}/stream'.format(id), headers={'x-token': self.token}, params=data)
        result = {
            'thread': 1,
            'created': 1388534400.0,
            'text': 'text', 'attach': None,
            'user': {'lastname': 'Test1',
                     'relation': 'u', 'id': 1,
                     'firstname': 'Test1',
                     'is_online': True},
            'id': 1}
        self.assertEqual(len(resp.json()), 1)
        self.assertDictEqual(resp.json()[0], result)

    def test_stat_get(self):
        resp = self.req_sess.get(self.fullpath+'/msgr/stat', headers={'x-token': self.token})
        param = {'new_msgs': 0}
        self.assertDictEqual(resp.json(), param)

    def test_create_put(self):
        text = 'test'
        data = {
            'user_ids': [1],
            'text': text
        }
        resp = self.req_sess.put(self.fullpath+'/msgr/create', headers={'x-token': self.token}, data=data)
        result = {
            'msgr_cnt': 1,
            'id': 3,
            'users': [
                {'lastname': 'Test1', 'relation': 'u', 'id': 1, 'firstname': 'Test1', 'is_online': True}
            ]
        }
        self.assertDictEqual(resp.json(), result)
        msg = self.session.query(MsgrLog).all()[-1]
        self.assertEqual(msg.text, text)
        self.assertEqual(msg.text, text)
        self.assertEqual(msg.msgr_threads_id, result['id'])
        self.assertEqual(msg.user_id, self.user_id)


    def test_list_get(self):
        result = {
            'msgr_cnt': 2,
            'id': 1,
            'users': [
                {'lastname': 'Test2','relation': 'u','id': 2,'firstname': 'Test2','is_online': False}
            ]
        }
        resp = self.req_sess.get(self.fullpath+'/msgr/list', headers={'x-token': self.token}, params={'user_author': [2]})
        self.assertDictEqual(resp.json()[0], result)

    def test_send_put(self):
        text = 'test_text'
        data = {
            u'text': text,
        }
        id = 2
        resp = self.req_sess.put(self.fullpath+'/msgr/{0}/send'.format(id), headers={'x-token': self.token}, data=data)
        m_log = self.session.query(MsgrLog).all()[-1]
        self.assertEqual(m_log.user_id, self.user_id)
        self.assertEqual(m_log.msgr_threads_id, id)
        self.assertEqual(m_log.text, text)
        self.assertEqual(resp.json(), {})

