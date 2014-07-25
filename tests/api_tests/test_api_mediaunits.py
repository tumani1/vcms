# coding: utf-8
import zerorpc
import unittest
from models import Base, SessionToken
from sqlalchemy.orm import sessionmaker, scoped_session
from utils.connection import db_connect, create_session
from tests.api_tests.fixtures import create_media_units, create_topic, create
from settings import CONFIG_PATH
from os.path import join
import yaml
import requests
import json


def setUpModule():
    engine = db_connect()
    session = create_session(bind=engine)

    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)
    create_topic(session)
    create_media_units(session)


def tearDownModule():
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")


class MediaUnitsTestCase(unittest.TestCase):

    def setUp(self):
        with open(join(CONFIG_PATH, 'node_service.yaml')) as file:
            conf = yaml.safe_load(file)
        self.h, self.p = conf['rest_ws_serv']['host'], conf['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)
        self.req_sess = requests.Session()
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.user_id = 1
        token_str = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'}).content
        self.token = json.loads(token_str)['token']

    def test_info(self):
        IPC_pack = {'api_group': 'mediaunits',
                    'api_method': 'info',
                    'http_method': 'get',
                    'api_format': 'json',
                    'x_token': self.session_token[1],
                    'query_params': {
                        'id': 2}}
        temp = {
            'id': 2,
            'title': 'mu2',
            'title_orig': 2,
            'description': 'test2',
            'prev': 1,
            'next': 3,
            'releasedate': 1325376000.0,
            'enddate': 1391212800.0,
            'batch': 'batch1',
            'relation': {'watched': 1388534400.0},
        }
        resp = self.cl.route(IPC_pack)
        self.assertDictEqual(resp, temp)

    def test_next(self):
        IPC_pack = {'api_group': 'mediaunits',
                    'api_method': 'next',
                    'http_method': 'get',
                    'api_format': 'json',
                    'x_token': self.session_token[1],
                    'query_params': {'id': 2,}
                    }
        temp = {
            'id': 3,
            'title': 'mu3',
            'title_orig': 3,
            'description': 'test3',
            'prev': 2,
            'next': None,
            'releasedate': 1356998400.0,
            'enddate': 1391212800.0,
            'batch': 'batch1',
            'relation': {},
        }
        resp = self.cl.route(IPC_pack)
        self.assertDictEqual(resp, temp)

    def test_prev(self):
        IPC_pack = {'api_group': 'mediaunits',
                    'api_method': 'prev',
                    'http_method': 'get',
                    'api_format': 'json',
                    'x_token': self.session_token[1],
                    'query_params': {'id': 3,}
                    }
        temp = {
            'id': 2,
            'title': 'mu2',
            'title_orig': 2,
            'description': 'test2',
            'prev': 1,
            'next': 3,
            'releasedate': 1325376000.0,
            'enddate': 1391212800.0,
            'batch': 'batch1',
            'relation': {'watched': 1388534400.0},
        }
        resp = self.cl.route(IPC_pack)
        self.assertDictEqual(resp, temp)

    def test_list(self):
        IPC_pack = {'api_group': 'mediaunits',
                    'api_method': 'list',
                    'http_method': 'get',
                    'api_format': 'json',
                    'x_token': self.session_token[1],
                    'query_params': {'text': 'mu1',}
                    }
        temp = {
            'id': 1,
            'title': 'mu1',
            'title_orig': 1,
            'description': 'test1',
            'prev': None,
            'next': 2,
            'releasedate': 1293840000.0,
            'enddate': 1391212800.0,
            'batch': 'batch1',
            'relation': {'watched': 1388534400.0},
        }
        resp = self.cl.route(IPC_pack)
        self.assertDictEqual(resp[0], temp)

    def tearDown(self):
        self.cl.close()
        self.session.remove()