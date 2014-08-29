# coding: utf-8
import unittest
import zerorpc

from models.base import Base
from tests.constants import INTERNAL_ZERORPC_SERVICE_URI
from tests.fixtures import create
from utils.connection import get_session, create_session, db_connect


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


class CdnApiTestCase(unittest.TestCase):
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

    def tearDown(self):
        self.session.close()
        self.zero_client.close()

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
