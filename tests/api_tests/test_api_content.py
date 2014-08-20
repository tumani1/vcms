import unittest
import zerorpc
from models import Base
from tests.constants import ZERORPC_SERVICE_URI
from tests.fixtures import create_content
from utils.connection import db_connect, create_session, get_session


def setUpModule():
    engine = db_connect().connect()
    engine.execute("drop schema public cascade; create schema public;")
    session = create_session(bind=engine)

    # Create table
    Base.metadata.create_all(bind=engine)

    create_content(session)

    engine.close()


class ContentInfoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = get_session()
        cls.zero_client = zerorpc.Client(timeout=3000, heartbeat=100000)
        cls.zero_client.connect(ZERORPC_SERVICE_URI)
        cls.ipc_pack = {
            'api_method': '',
            'api_type': 'get',
            'x_token': None,
            'query_params': {}
        }

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        cls.zero_client.close()

    def test_get_info(self):
        ContentInfoTestCase.ipc_pack['api_method'] = '/content/1/info'
        ContentInfoTestCase.ipc_pack['api_type'] = 'get'
        resp = self.zero_client.route(ContentInfoTestCase.ipc_pack)
        result = {
            u'text': u'test',
            u'id': 1,
            u'title': None
        }
        self.assertDictEqual(resp, result)

class ContentListTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = get_session()
        cls.zero_client = zerorpc.Client(timeout=3000, heartbeat=100000)
        cls.zero_client.connect(ZERORPC_SERVICE_URI)
        cls.ipc_pack = {
            'api_method': '',
            'api_type': 'get',
            'x_token': None,
            'query_params': {}
        }

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        cls.zero_client.close()

    def test_get_list(self):
        ContentListTestCase.ipc_pack['api_method'] = '/content/list'
        ContentListTestCase.ipc_pack['api_type'] = 'get'
        resp = self.zero_client.route(ContentListTestCase.ipc_pack)
        result = {
            u'text': u'test',
            u'id': 1,
            u'title': None
        }
        self.assertDictEqual(resp[0], result)



