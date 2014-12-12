import zerorpc
import unittest

from sqlalchemy.orm import sessionmaker, scoped_session

from models import Base, SessionToken, MsgrLog

from utils.connection import db_connect, create_session

from tests.constants import ZERORPC_SERVICE_URI
from tests.fixtures import create, create_msgr_threads, create_users_msgr_threads, create_msgr_log


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
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.cl = zerorpc.Client(timeout=3000, heartbeat=100000)
        self.cl.connect(ZERORPC_SERVICE_URI)
        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)

    def tearDown(self):
        self.cl.close()
        self.session.close()

    def test_info_get(self):
        id = 1
        IPC_pack = {
            'api_method': '/msgr/%s/info' % (id),
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {}
        }
        resp = self.cl.route(IPC_pack)
        temp = {
            'msgr_cnt': 2,
            'id': 1,
            'users': [
                {'lastname': 'Test2','relation': 'u','id': 2,'firstname': 'Test2','is_online': False}
            ]
        }
        self.assertDictEqual(resp, temp)

    def test_stat_get(self):
        IPC_pack = {
            'api_method': '/msgr/stat',
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {}
        }
        resp = self.cl.route(IPC_pack)
        param = {'new_msgs': 0}
        self.assertDictEqual(resp, param)

    def test_create_put(self):
        text = 'test'
        IPC_pack = {
            'api_method': '/msgr/create',
            'api_type': 'put',
            'x_token': self.session_token[1],
            'query_params': {'user_ids': [1], 'text': text}
        }
        temp = {
            'msgr_cnt': 1,
            'id': 3,
            'users': [
                {'lastname': 'Test1', 'relation': 'u', 'id': 1, 'firstname': 'Test1', 'is_online': True}
            ]
        }
        resp = self.cl.route(IPC_pack)
        self.assertDictEqual(resp, temp)
        msg = self.session.query(MsgrLog).all()[-1]
        self.assertEqual(msg.text, text)
        self.assertEqual(msg.text, text)
        self.assertEqual(msg.msgr_threads_id, temp['id'])
        self.assertEqual(msg.user_id, self.user_id)

    def test_list_get(self):
        IPC_pack = {
            'api_method': '/msgr/list',
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {'user_author': [2]}
        }
        temp = {
            'msgr_cnt': 2,
            'id': 1,
            'users': [
                {'lastname': 'Test2','relation': 'u','id': 2,'firstname': 'Test2','is_online': False}
            ]
        }
        resp = self.cl.route(IPC_pack)
        self.assertEqual(len(resp), 1)
        self.assertDictEqual(resp[0], temp)

    def test_stream_get(self):
        id = 1
        IPC_pack = {
            'api_method': '/msgr/%s/stream' % (id),
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {}
        }
        temp = {
            'thread': 1,
            'created': 1388534400.0,
            'text': 'text', 'attach': None,
            'user': {'lastname': 'Test1',
                     'relation': 'u', 'id': 1,
                     'firstname': 'Test1',
                     'is_online': True},
            'id': 1}

        resp = self.cl.route(IPC_pack)
        self.assertEqual(len(resp), 1)
        self.assertDictEqual(resp[0], temp)

    def test_send_put(self):
        id = 2
        text = 'test_text'
        IPC_pack = {
            'api_method': '/msgr/%s/send' % (id),
            'api_type': 'put',
            'x_token': self.session_token[1],
            'query_params': {'text': text}
        }
        resp = self.cl.route(IPC_pack)
        m_log = self.session.query(MsgrLog).all()[-1]
        self.assertEqual(m_log.user_id, self.user_id)
        self.assertEqual(m_log.msgr_threads_id, id)
        self.assertEqual(m_log.text, text)
        self.assertEqual(resp, {})