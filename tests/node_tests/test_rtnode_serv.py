# coding=utf-8
import unittest
import yaml
import requests
import json
from settings import CONFIG_PATH
from os.path import join
from tests.create_test_user import create
from websocket import create_connection


class RestTemplateNodeServiceTestCase(unittest.TestCase):

    def setUp(self):
        with open(join(CONFIG_PATH, 'node_service.yaml')) as file:
            conf = yaml.safe_load(file)
        self.h, self.p = conf['rest_serv']['host'], conf['rest_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)
        self.session = requests.Session()
        self.ws = create_connection('ws://{}:{}'.format(self.h, self.p))
        create()

    def test_echo_get(self):
        resp = self.session.get(self.fullpath+'/test/echo?message=hello')
        self.assertEqual(resp.json(), {'message': 'hello'})

    def test_echo_put(self):
        data = {'message': 'hello'}
        resp = self.session.put(self.fullpath+'/test/echo', data=data)
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
