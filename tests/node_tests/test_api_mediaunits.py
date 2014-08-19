# coding: utf-8
import json
import unittest
import requests
from sqlalchemy.orm import sessionmaker, scoped_session

from models import Base
from utils.connection import db_connect, create_session
from tests.fixtures import create_media_units, create_topic, create
from tests.constants import NODE


def setUpModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")
    session = create_session(bind=engine)

    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)
    create_topic(session)
    create_media_units(session)


def tearDownModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")


class MediaUnitsTestCase(unittest.TestCase):

    def setUp(self):
        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)
        self.req_sess = requests.Session()
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.user_id = 1
        token_str = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'}).content
        self.token = json.loads(token_str)['token']

    def test_info(self):
        id = 2
        data = {}
        resp = self.req_sess.get(self.fullpath+'/mediaunits/%s/info' % (id), headers={'token': self.token}, params=data)
        temp = {
            u'enddate': 1391212800,
            u'description': u'test2',
            u'title': u'mu2',
            u'batch': u'batch1',
            u'next': 3,
            u'releasedate': 1325376000,
            u'title_orig': u'2',
            u'relation': {u'watched': 1388534400},
            u'prev': 1,
            u'id': 2
        }
        self.assertDictEqual(resp.json(), temp)

    def test_next(self):
        id = 2
        data = {}
        resp = self.req_sess.get(self.fullpath+'/mediaunits/%s/next' % (id), headers={'token': self.token}, params=data)
        temp = {
            u'enddate': 1391212800,
            u'description': u'test3',
            u'title': u'mu3',
            u'batch': u'batch1',
            u'next': None,
            u'releasedate': 1356998400,
            u'title_orig': u'3',
            u'relation': {},
            u'prev': 2,
            u'id': 3
        }
        self.assertDictEqual(resp.json(), temp)

    def test_prev(self):
        data = {}
        id = 3
        resp = self.req_sess.get(self.fullpath+'/mediaunits/%s/prev' % (id), headers={'token': self.token}, params=data)
        temp = {
            u'enddate': 1391212800,
            u'description': u'test2',
            u'title': u'mu2',
            u'batch': u'batch1',
            u'next': 3,
            u'releasedate': 1325376000,
            u'title_orig': u'2',
            u'relation': {u'watched': 1388534400},
            u'prev': 1,
            u'id': 2
        }
        self.assertDictEqual(resp.json(), temp)

    def test_list(self):
        data = {'text': 'mu1'}
        resp = self.req_sess.get(self.fullpath+'/mediaunits/list', headers={'token': self.token}, params=data)
        temp = [{
                    u'enddate': 1391212800,
                    u'description': u'test1',
                    u'title': u'mu1',
                    u'batch': u'batch1',
                    u'next': 2,
                    u'releasedate': 1293840000,
                    u'title_orig': u'1',
                    u'relation': {u'watched': 1388534400},
                    u'prev': None,
                    u'id': 1
                }]
        self.assertListEqual(resp.json(), temp)

    def tearDown(self):
        self.session.remove()
