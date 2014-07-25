# coding=utf-8
import unittest
import requests
import json
from settings import NODE
from tests.create_test_user import create
from websocket import create_connection
from utils.connection import get_session


class RestWsNodeServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)
        self.req_sess = requests.Session()
        self.ws = create_connection('ws://{}:{}'.format(self.h, self.p))
        db_sess = get_session()
        create(db_sess)

    def test_echo_get(self):
        resp = self.req_sess.get(self.fullpath+'/test/echo?message=hello')
        self.assertEqual(resp.json(), {'message': 'hello'})

    def test_echo_put(self):
        data = {'message': 'hello'}
        resp = self.req_sess.put(self.fullpath+'/test/echo', data=data)
        self.assertEqual(resp.json(), data)

    def test_ws_echo_get(self):
        IPC_pack = {'api_group': 'test',
                    'api_method': 'echo',
                    'http_method': 'get',
                    'query_params': {'text': 'FROM TEST'}}
        self.ws.send(json.dumps(IPC_pack))
        resp = self.ws.recv()
        self.assertEqual(json.loads(resp), IPC_pack['query_params'])

    def tearDown(self):
        self.ws.close()