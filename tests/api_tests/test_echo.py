import zerorpc
import unittest
from tests.create_test_user import create

class ZeroRpcServiceTestCase(unittest.TestCase):

    
    def setUp(self):
        self.cl = zerorpc.Client()
        self.cl.connect("tcp://127.0.0.1:4242")
        create()

    def test_echo(self):
        IPC_pack = {'api_group':'test',
                    'api_method':'echo',
                    'http_method':'put',
                    'token':'echo_token',
                    'query_params':{
                        'message':'hello'}}
        resp = self.cl.route(IPC_pack)
        self.assertEqual(IPC_pack['query_params'], resp)

    def tearDown(self):
        self.cl.close()
