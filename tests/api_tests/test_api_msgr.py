import zerorpc
import unittest

from sqlalchemy.orm import sessionmaker, scoped_session

from models import Base, SessionToken

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
            'query_params': {
                'x_token': self.session_token[1],
            }
        }
        resp = self.cl.route(IPC_pack)

    def test_stat_get(self):
        IPC_pack = {
            'api_method': '/msgr/stat',
            'api_type': 'get',
            'query_params': {
                'x_token': self.session_token[1],
            }
        }
        resp = self.cl.route(IPC_pack)
        param = {'new_msgs': 1}
        self.assertDictEqual(resp, param)

    def test_create_put(self):
        IPC_pack = {
            'api_method': '/msgr/create',
            'api_type': 'put',
            'query_params': {
                'user_ids': [1, 2],
                'text': 'test',
                'x_token': self.session_token[1],}
        }
        resp = self.cl.route(IPC_pack)

    def test_list_get(self):
        IPC_pack = {
            'api_method': '/msgr/list',
            'api_type': 'get',
            'query_params': {
                'user_author': [1, 2],
                'x_token': self.session_token[1],}
        }
        resp = self.cl.route(IPC_pack)
