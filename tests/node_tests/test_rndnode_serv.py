# coding=utf-8
import unittest
import requests

from tests.constants import NODE


class RestTemplateNodeServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.session = requests.Session()

    def test_get_index_page(self):
        host, port = NODE['render_serv']['host'], NODE['render_serv']['port']
        resp = self.session.get('http://{}:{}/index.html'.format(host, port))
        self.assertIn('From jade template', resp.text)