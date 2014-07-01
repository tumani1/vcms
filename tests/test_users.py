# coding: utf-8
import zerorpc
import unittest


class UsersTestCase(unittest.TestCase):
    def setUp(self):
        self.client = zerorpc.Client()
        self.client.connect("tcp://")