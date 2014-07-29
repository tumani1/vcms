import unittest
import requests


class ContentInfoTestCase(unittest.TestCase):

    def test_get_info(self):
        resp = requests.get('http://127.0.0.1:9977/content/1/info')
        self.assertEqual(resp.json(), 1)


class ContentListTestCase(unittest.TestCase):

    def test_get_list(self):
        resp = requests.get('http://127.0.0.1:9977/content/list')
        self.assertEqual(resp.json(), 1)