#

import zerorpc
import unittest

from utils.connection import db_connect, create_session

from tests.create_test_user import create
from tests.constants import ZERORPC_SERVICE_URI


class ZeroRpcServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.cl = zerorpc.Client()
        self.cl.connect(ZERORPC_SERVICE_URI)
        engine = db_connect()
        session = create_session(bind=engine)
        create(session)


    def test_echo(self):
        IPC_pack = {'api_group': 'test',
                    'api_method': 'echo',
                    'http_method': 'put',
                    'token': 'echo_token',
                    'query_params': {'message': 'hello'}}
        resp = self.cl.route(IPC_pack)
        self.assertEqual(IPC_pack['query_params'], resp)


    def tearDown(self):
        self.cl.close()
