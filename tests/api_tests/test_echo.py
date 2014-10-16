# coding: utf-8
import zerorpc
import unittest

from utils.connection import db_connect
from models.base import Base
from tests.constants import ZERORPC_SERVICE_URI


def setUpModule():
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")
    Base.metadata.create_all(bind=engine)


class ZeroRpcServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.cl = zerorpc.Client()
        self.cl.connect(ZERORPC_SERVICE_URI)

    def test_echo(self):
        IPC_pack = {
                    'api_method': '/test/echo',
                    'api_type': 'put',
                    'token': 'echo_token',
                    'query_params': {'message': 'hello'}}
        resp = self.cl.route(IPC_pack)
        self.assertEqual(IPC_pack['query_params'], resp)


    def tearDown(self):
        self.cl.close()
