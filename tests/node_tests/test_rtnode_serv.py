# coding: utf-8
import json
import unittest
import requests

from tests.constants import NODE
from websocket import create_connection
from utils.connection import get_session


class RestWsNodeServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)
        self.req_sess = requests.Session()
        self.ws = create_connection('ws://{}:{}'.format(self.h, self.p))
        self.db_sess = get_session()

    def test_echo_get(self):
        params = {'message': 'hello'}
        resp = self.req_sess.get(self.fullpath+'/test/echo', params=params)
        self.assertEqual(resp.json(), {'message': 'hello'})

    def test_error_get(self):
        resp = self.req_sess.get(self.fullpath+'/some/some?message=hello')
        self.assertEqual(resp.status_code, 404)

    def test_echo_put(self):
        data = {'message': 'hello'}
        resp = self.req_sess.put(self.fullpath+'/test/echo', data=data)
        self.assertEqual(resp.json(), data)

    def test_error_put(self):
        data = {'message': 'hello'}
        resp = self.req_sess.put(self.fullpath+'/some/some', data=data)
        self.assertEqual(resp.status_code, 404)

    def test_ws_echo_get(self):
        IPC_pack = {'api_method': '/test/echo',
                    'api_type': 'get',
                    'query_params': {'text': 'FROM TEST'}}
        self.ws.send(json.dumps(IPC_pack))
        resp = self.ws.recv()
        self.assertEqual(json.loads(resp), IPC_pack['query_params'])

    def test_ws_error(self):
        IPC_pack = {'api_method': '/some/some',
                    'api_type': 'get',
                    'query_params': {'text': 'FROM TEST'}}
        self.ws.send(json.dumps(IPC_pack))
        resp = self.ws.recv()
        resp = json.loads(resp)
        self.assertEqual(resp['code'], 404)
        self.assertEqual(resp['message'], 'Not Found')

    def tearDown(self):
        self.ws.close()
        self.db_sess.close()