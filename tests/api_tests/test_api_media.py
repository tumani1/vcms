# coding: utf-8
import unittest
import zerorpc

from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker, scoped_session
from settings import DATABASE

from tests.constants import ZERORPC_SERVICE_URI
from models import Base, UsersMedia, SessionToken
from utils.connection import db_connect, create_session, mongo_connect
from tests.fixtures import create_media_units, create_topic, create, create_media, create_persons


def setUpModule():
    mongo_engine = mongo_connect()
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")
    mongo_engine.drop_database(DATABASE['mongodb']['db'])
    session = create_session(bind=engine)

    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)
    create_topic(session)
    create_media_units(session)
    create_persons(session)
    create_media(session)


def tearDownModule():
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")


class MediaTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.cl = zerorpc.Client(timeout=3000, heartbeat=100000)
        self.cl.connect(ZERORPC_SERVICE_URI, )
        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)

    def test_info(self):
        id = 1
        IPC_pack = {'api_method': '/media/%s/info'  % (id),
                    'api_type': 'get',
                    'x_token': self.session_token[1],
                    'query_params': {}
        }
        temp = {
            'rating': 0.0,
            'description': 'test_desc1',
            'title': 'media1', 'locations': [],
            'id': 1,
            'releasedate': None,
            'duration': None,
            'title_orig': 'test_media1',
            'units': [
                {
                    'topic': {
                        'name': 'test1',
                        'title': 'test1',
                        'releasedate': 1388534400.0,
                        'relation': {
                            'liked': 0,
                            'subscribed': False
                        },
                    'title_orig': None,
                    'type': 'news'
                    },
                'title_orig': '2',
                'relation': {'watched': 1388534400.0},
                'id': 2,
                'title': 'mu2'
                }
            ],
            'relation': {'watched': 1356998400.0, 'liked': 1388534400.0, 'playlist': 50, 'pos': 50},
            'rating_votes': 0,
            'views_cnt': 0
        }
        resp = self.cl.route(IPC_pack)
        self.assertDictEqual(resp, temp)

    def test_list(self):
        IPC_pack = {
                    'api_method': '/media/list',
                    'api_type': 'get',
                    'x_token': self.session_token[1],
                    'query_params': {'text': u'media1'}
        }
        temp = [
                {
                    'rating': 0.0,
                    'description': 'test_desc1',
                    'title': 'media1', 'locations': [],
                    'id': 1,
                    'releasedate': None,
                    'duration': None,
                    'title_orig': 'test_media1',
                    'units': [
                        {
                            'topic': {
                                'name': 'test1',
                                'title': 'test1',
                                'releasedate': 1388534400.0,
                                'relation': {
                                    'liked': 0,
                                    'subscribed': False
                                },
                            'title_orig': None,
                            'type': 'news'
                            },
                        'title_orig': '2',
                        'relation': {'watched': 1388534400.0},
                        'id': 2,
                        'title': 'mu2'
                        }
                    ],
                    'relation': {'watched': 1356998400.0, 'liked': 1388534400.0, 'playlist': 50, 'pos': 50},
                    'rating_votes': 0,
                    'views_cnt': 0
            }
        ]
        resp = self.cl.route(IPC_pack)
        self.assertListEqual(resp, temp)

    def test_media_persons(self):
        id = 1
        IPC_pack = {
                    'api_method': '/media/%s/persons' % (id),
                    'api_type': 'get',
                    'x_token': self.session_token[1],
                    'query_params': {}
        }
        temp = [{
                    'firstname': 'test',
                    'lastname': 'testov',
                    'relation': {},
                    'user': {
                        'lastvisit': '',
                        'city': 'Test',
                        'firstname': 'Test1',
                        'gender': 'n',
                        'is_online': True,
                        'regdate': 1325376000.0,
                        'lastname': 'Test1',
                        'country': u'Russian Federation',
                        'id': 1,
                        'relation': 'u',
                        'person_id': 1},
                    'role': 'actor',
                    'type': '',
                    'id': 1
                }]
        resp = self.cl.route(IPC_pack)
        self.assertListEqual(resp, temp)

    def test_media_units(self):
        id = 1
        IPC_pack = {
                    'api_method': '/media/%s/units' % (id),
                    'api_type': 'get',
                    'x_token': self.session_token[1],
                    'query_params': {}
        }
        temp = [
            {
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
                'title': 'mu2', 'batch': 'batch1',
                'next': 3, 'releasedate': 1325376000.0,
                'title_orig': '2',
                'relation': {'watched': 1388534400.0},
                'prev': 1,
                'id': 2
            }
        ]
        resp = self.cl.route(IPC_pack)
        self.assertListEqual(resp, temp)

    def test_media_like_get(self):
        id = 3
        IPC_pack = {
                    'api_method': '/media/%s/like' % (id),
                    'api_type': 'get',
                    'x_token': self.session_token[1],
                    'query_params': {}
        }
        temp = {"liked":0}
        resp = self.cl.route(IPC_pack)
        self.assertDictEqual(resp, temp)

    def test_media_like_post(self):
        id = 2
        IPC_pack = {
                    'api_method': '/media/%s/like' % (id),
                    'api_type': 'post',
                    'x_token': self.session_token[1],
                    'query_params': {}
        }
        resp = self.cl.route(IPC_pack)
        um = self.session.query(UsersMedia).filter(and_(UsersMedia.user_id==self.user_id, UsersMedia.media_id==id)).first()
        self.assertTrue(um.liked)

    def test_media_like_delete(self):
        id = 4
        IPC_pack = {
                    'api_method': '/media/%s/like' % (id),
                    'api_type': 'delete',
                    'x_token': self.session_token[1],
                    'query_params': {}
        }
        resp = self.cl.route(IPC_pack)
        um = self.session.query(UsersMedia).filter(and_(UsersMedia.user_id==self.user_id, UsersMedia.media_id==id)).first()
        self.assertFalse(um.liked)

    def test_media_playlist_get(self):
        id = 3
        IPC_pack = {
                    'api_method': '/media/%s/playlist' % (id),
                    'api_type': 'get',
                    'x_token': self.session_token[1],
                    'query_params': {}
        }
        resp = self.cl.route(IPC_pack)
        temp = {"in_playlist":1391212800}
        self.assertDictEqual(resp, temp)

    def test_media_playlist_post(self):
        id = 2
        IPC_pack = {
                    'api_method': '/media/%s/playlist' % (id),
                    'api_type': 'post',
                    'x_token': self.session_token[1],
                    'query_params': {}
        }
        resp = self.cl.route(IPC_pack)
        um = self.session.query(UsersMedia).filter(and_(UsersMedia.user_id==self.user_id, UsersMedia.media_id==id)).first()
        self.assertTrue(um.playlist)

    def test_media_playlist_delete(self):
        id = 4
        IPC_pack = {
                    'api_method': '/media/%s/playlist' % (id),
                    'api_type': 'delete',
                    'x_token': self.session_token[1],
                    'query_params': {}
        }
        resp = self.cl.route(IPC_pack)
        um = self.session.query(UsersMedia).filter(and_(UsersMedia.user_id==self.user_id, UsersMedia.media_id==id)).first()
        self.assertFalse(um.playlist)

    def test_media_state_get(self):
        id = 3
        IPC_pack = {
                    'api_method': '/media/%s/state' % (id),
                    'api_type': 'get',
                    'x_token': self.session_token[1],
                    'query_params': {}
        }
        resp = self.cl.route(IPC_pack)
        temp = {"watched":1388534400,"pos":20}
        self.assertDictEqual(resp, temp)

    def test_media_state_post(self):
        id = 2
        IPC_pack = {
                    'api_method': '/media/%s/state' % (id),
                    'api_type': 'post',
                    'x_token': self.session_token[1],
                    'query_params': {'pos': 20}
        }
        resp = self.cl.route(IPC_pack)
        um = self.session.query(UsersMedia).filter(and_(UsersMedia.user_id==self.user_id, UsersMedia.media_id==id)).first()
        self.assertEqual(um.play_pos, IPC_pack['query_params']['pos'])

    def test_media_state_delete(self):
        id = 4
        IPC_pack = {
                    'api_method': '/media/%s/state' % (id),
                    'api_type': 'delete',
                    'x_token': self.session_token[1],
                    'query_params': {}
        }
        resp = self.cl.route(IPC_pack)
        um = self.session.query(UsersMedia).filter(and_(UsersMedia.user_id==self.user_id, UsersMedia.media_id==id)).first()
        self.assertFalse(um.watched)
        self.assertFalse(um.play_pos)

    def tearDown(self):
        self.session.remove()