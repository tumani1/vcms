import httplib
import unittest
import yaml


class RestTemplateNodeServiceTestCase(unittest.TestCase):

    def setUp(self):
        with open('../configs/node_service.yaml') as file:
            conf = yaml.safe_load(file)
        self.conn = httplib.HTTPConnection(conf['address'], conf['port'])

    def test_echo_get(self):


    def test_echo_put(self):
        pass

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
