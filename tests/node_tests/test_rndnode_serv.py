# coding=utf-8
import unittest
import yaml
import requests
from settings import CONFIG_PATH
from os.path import join


class RestTemplateNodeServiceTestCase(unittest.TestCase):

    def setUp(self):
        with open(join(CONFIG_PATH, 'node_service.yaml')) as file:
            self.conf = yaml.safe_load(file)
        self.session = requests.Session()

    def test_get_index_page(self):
        host, port = self.conf['render_serv']['host'], self.conf['render_serv']['port']
        resp = self.session.get('http://{}:{}/index.html'.format(host, port))
        self.assertIn('From jade template', resp.text)