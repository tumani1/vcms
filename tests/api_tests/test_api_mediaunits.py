import zerorpc
import unittest
from models import Base, SessionToken
from sqlalchemy.orm import sessionmaker, scoped_session
from utils.connection import db_connect, create_session

from tests.constants import ZERORPC_SERVICE_URI
from tests.fixtures import create_media_units, create_topic, create


def setUpModule():
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
    engine.execute("drop schema public cascade; create schema public;")


class MediaUnitsTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.cl = zerorpc.Client(timeout=3000)
        self.cl.connect(ZERORPC_SERVICE_URI, )
        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)

    def test_info(self):
        id = 2
        IPC_pack = {
                    'api_method': '/mediaunits/%s/info' % (id),
                    'api_type': 'get',
                    'x_token': self.session_token[1],
                    'query_params': {}
        }
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
        resp = self.cl.route(IPC_pack)
        self.assertDictEqual(resp, temp)

    def test_next(self):
        id = 2
        IPC_pack = {
                    'api_method': '/mediaunits/%s/next' % (id),
                    'api_type': 'get',
                    'x_token': self.session_token[1],
                    'query_params': {}
                    }
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
        resp = self.cl.route(IPC_pack)
        self.assertDictEqual(resp, temp)

    def test_prev(self):
        id = 3
        IPC_pack = {
                    'api_method': '/mediaunits/%s/prev' % (id),
                    'api_type': 'get',
                    'x_token': self.session_token[1],
                    'query_params': {}
                    }
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
        resp = self.cl.route(IPC_pack)
        self.assertDictEqual(resp, temp)

    def test_list(self):
        IPC_pack = {
                    'api_method': '/mediaunits/list',
                    'api_type': 'get',
                    'x_token': self.session_token[1],
                    'query_params': {'text': 'mu1',}
                    }
        temp =  {
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
        resp = self.cl.route(IPC_pack)
        self.assertDictEqual(resp[0], temp)

    def tearDown(self):
        self.cl.close()
        self.session.remove()
