import unittest
import yaml
import json
import requests
from settings import CONFIG_PATH
from os.path import join
from create_test_user import create


class RestTemplateNodeServiceTestCase(unittest.TestCase):

    def setUp(self):
        with open(join(CONFIG_PATH, 'node_service.yaml')) as file:
            conf = yaml.safe_load(file)
        self.fullpath = 'http://{}:{}'.format(conf['host'], conf['port'])
        create()

    def test_echo_get(self):
        resp = requests.get(self.fullpath+'/test/echo?message=hello')
        self.assertEqual(resp.json(), {'message': 'hello'})

    @unittest.skipUnless('надо поправить обработку PUT в node')
    def test_echo_put(self):
        data = {'message': 'hello'}
        resp = requests.put(self.fullpath+'/test/echo', data=data)
        self.assertEqual(resp.json(), {'message': 'hello'})