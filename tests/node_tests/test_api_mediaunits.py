# coding: utf-8
import json
import unittest
import requests
from sqlalchemy.orm import sessionmaker, scoped_session

from models import Base, SessionToken
from settings import DATABASE
from utils.connection import db_connect, create_session, mongo_connect
from tests.fixtures import create_media_units, create_topic, create
from tests.constants import NODE


def setUpModule():
    mongo_engine = mongo_connect()
    mongo_engine.drop_database(DATABASE['mongodb']['db'])
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")
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
        self.token = SessionToken.generate_token(self.user_id, session=self.session)[1]

    def test_info(self):
        id = 2
        data = {}
        resp = self.req_sess.get(self.fullpath+'/mediaunits/{0}/info'.format(id), headers={'x-token': self.token}, params=data)
        temp = {
            'topic': {
                'description': 'test test',
                'title': 'test1',
                'releasedate': 1388534400.0,
                'relation': {'liked': 0, 'subscribed': False},
                'title_orig': None,
                'type': 'news',
                'name': 'test1'
            },
            'enddate': 1391212800.0,
            'description': 'test2',
            'title': 'mu2',
            'batch': 'batch1',
            'next': 3,
            'releasedate': 1325376000.0,
            'title_orig': '2',
            'relation': {'watched': 1388534400.0},
            'prev': 1,
            'id': 2
        }
        self.assertDictEqual(resp.json(), temp)

    def test_next(self):
        id = 2
        data = {}
        resp = self.req_sess.get(self.fullpath+'/mediaunits/{0}/next'.format(id), headers={'x-token': self.token}, params=data)
        temp = {
            'topic': {
                'description': 'test test',
                'title': 'test1',
                'releasedate': 1388534400.0,
                'relation': {'liked': 0, 'subscribed': False},
                'title_orig': None,
                'type': 'news',
                'name': 'test1'
            },
            'enddate': 1391212800.0,
            'description': 'test3',
            'title': 'mu3',
            'batch': 'batch1',
            'next': None,
            'releasedate': 1356998400.0,
            'title_orig': '3',
            'relation': {},
            'prev': 2,
            'id': 3
        }
        self.assertDictEqual(resp.json(), temp)

    def test_prev(self):
        data = {}
        id = 3
        resp = self.req_sess.get(self.fullpath+'/mediaunits/{0}/prev'.format(id), headers={'x-token': self.token}, params=data)
        temp = {
            'topic': {
                'description': 'test test',
                'title': 'test1',
                'releasedate': 1388534400.0,
                'relation': {'liked': 0, 'subscribed': False},
                'title_orig': None,
                'type': 'news',
                'name': 'test1'
            },
            'enddate': 1391212800.0,
            'description': 'test2',
            'title': 'mu2',
            'batch': 'batch1',
            'next': 3,
            'releasedate': 1325376000.0,
            'title_orig': '2',
            'relation': {'watched': 1388534400.0},
            'prev': 1,
            'id': 2
        }
        self.assertDictEqual(resp.json(), temp)

    def test_list(self):
        data = {'text': 'mu1'}
        resp = self.req_sess.get(self.fullpath+'/mediaunits/list', headers={'x-token': self.token}, params=data)
        temp = {
                'topic': {
                    'description': 'test test',
                    'title': 'test1',
                    'releasedate': 1388534400.0,
                    'relation': {'liked': 0, 'subscribed': False},
                    'title_orig': None,
                    'type': 'news',
                    'name': 'test1'
                },
                'enddate': 1391212800.0,
                'description': 'test1',
                'title': 'mu1',
                'batch': 'batch1',
                'next': 2,
                'releasedate': 1293840000.0,
                'title_orig': '1',
                'relation': {'watched': 1388534400.0},
                'prev': None,
                'id': 1
            }
        self.assertEqual(len(resp.json()), 1)
        self.assertDictEqual(resp.json()[0], temp)

    def tearDown(self):
        self.session.remove()
