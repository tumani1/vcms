# coding: utf-8

import zerorpc
import unittest
import datetime

from create_test_user import create_topic


class TopicTestCase(unittest.TestCase):

    def setUp(self):
        self.cl = zerorpc.Client()
        self.cl.connect("tcp://127.0.0.1:4242")
        create_topic()

    def test_echo(self):
        IPC_pack = {
            "api_group": "topics",
            "api_method":"info",
            "api_format":"json",
            "token":"echo_token",
            "http_method":"get",
            "query_params":{
                "name": "test"
            }
        }

        resp = self.cl.route(IPC_pack)
        temp = {
            'name': 'test11',
            'title': 'test',
            'title_orig': None,
            'description': 'test test',
            'releasedate': datetime.datetime(2014,1,1,0,0,0),
            'type': 'news',
            'relation': {
                'subscribed': False,
                'liked': 0,
            }
        }

        print resp
        self.assertEqual(temp, resp)

    def tearDown(self):
        self.cl.close()
