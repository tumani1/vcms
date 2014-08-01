# coding: utf-8
import unittest
import json

from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker, scoped_session
import requests

from models import Base, UsersMedia
from utils.connection import db_connect, create_session
from tests.fixtures import create_media_units, create_topic, create, create_media, create_persons
from settings import NODE


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
    create_persons(session)
    create_media(session)


def tearDownModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")


class MediaTestCase(unittest.TestCase):

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
        data = {'id': 1}
        resp = self.req_sess.get(self.fullpath+'/media/info', headers={'token': self.token}, params=data)
        temp = {
            u'description': u'test_desc1',
            u'title': u'media1',
            u'locations': [],
            u'releasedate': None,
            u'title_orig': u'test_media1',
            u'duration': None,
            u'relation': {u'watched': 1356998400, u'liked': 1388534400, u'pos': 50},
            u'id': 1
        }
        self.assertDictEqual(resp.json(), temp)

    def test_list(self):
        data = {'text': u'media1'}
        resp = self.req_sess.get(self.fullpath+'/media/list', headers={'token': self.token}, params=data)
        temp = [{
                    u'description': u'test_desc1',
                    u'title': u'media1',
                    u'locations': [],
                    u'releasedate': None,
                    u'title_orig': u'test_media1',
                    u'duration': None,
                    u'relation': {u'watched': 1356998400, u'liked': 1388534400, u'pos': 50},
                    u'id': 1
                }]
        self.assertListEqual(resp.json(), temp)

    def test_media_persons(self):
        data = {'id': 1}
        resp = self.req_sess.get(self.fullpath+'/media/persons', headers={'token': self.token}, params=data)
        temp = [{
                    u'firstname': u'test',
                    u'lastname': u'testov',
                    u'relation': {},
                    u'user': {u'lastvisit': u'', u'city': u'Test', u'firstname': u'Test1', u'gender': u'n', u'is_online': False, u'regdate': 1325376000, u'lastname': u'Test1', u'country': u'Test', u'id': 1},
                    u'role': u'actor',
                    u'type': u'',
                    u'id': 1
                }]
        self.assertListEqual(resp.json(), temp)

    def test_media_units(self):
        data = {'id': 1}
        resp = self.req_sess.get(self.fullpath+'/media/units', headers={'token': self.token}, params=data)
        temp = [{
                    u'enddate': 1391212800,
                    u'description': u'test2',
                    u'title': u'mu2',
                    u'batch': u'batch1',
                    u'next': 3,
                    u'releasedate': 1325376000,
                    u'title_orig': 2,
                    u'relation': {u'watched': 1388534400},
                    u'prev': 1,
                    u'id': 2
                }]
        self.assertListEqual(resp.json(), temp)

    def test_media_like_get(self):
        data = {'id': 3}
        resp = self.req_sess.get(self.fullpath+'/media/like', headers={'token': self.token}, params=data)
        temp = '{"liked":0}'
        self.assertEqual(resp.content, temp)

    def test_media_like_post(self):
        data = {'id': 2}
        resp = self.req_sess.post(self.fullpath+'/media/like', headers={'token': self.token}, params=data)
        um = self.session.query(UsersMedia).filter(and_(UsersMedia.user_id==self.user_id, UsersMedia.media_id==data['id'])).first()
        self.assertTrue(um.liked)

    def test_media_like_delete(self):
        data = {'id': 4}
        resp = self.req_sess.delete(self.fullpath+'/media/like', headers={'token': self.token}, params=data)
        um = self.session.query(UsersMedia).filter(and_(UsersMedia.user_id==self.user_id, UsersMedia.media_id==data['id'])).first()
        self.assertFalse(um.liked)

    def test_media_playlist_get(self):
        data = {'id': 3}
        resp = self.req_sess.get(self.fullpath+'/media/playlist', headers={'token': self.token}, params=data)
        temp = {"in_playlist":1391212800}
        self.assertEqual(resp.json(), temp)

    def test_media_playlist_post(self):
        data = {'id': 2}
        resp = self.req_sess.post(self.fullpath+'/media/playlist', headers={'token': self.token}, params=data)
        um = self.session.query(UsersMedia).filter(and_(UsersMedia.user_id==self.user_id, UsersMedia.media_id==data['id'])).first()
        self.assertTrue(um.playlist)

    def test_media_playlist_delete(self):
        data = {'id': 4}
        resp = self.req_sess.delete(self.fullpath+'/media/playlist', headers={'token': self.token}, params=data)
        um = self.session.query(UsersMedia).filter(and_(UsersMedia.user_id==self.user_id, UsersMedia.media_id==data['id'])).first()
        self.assertFalse(um.playlist)

    def test_media_state_get(self):
        data = {'id': 3}
        resp = self.req_sess.get(self.fullpath+'/media/state', headers={'token': self.token}, params=data)
        temp = {"watched":1388534400,"pos":20}
        self.assertEqual(resp.json(), temp)

    def test_media_state_post(self):
        data = {'id': 2, 'pos': 20}
        resp = self.req_sess.post(self.fullpath+'/media/state', headers={'token': self.token}, params=data)
        um = self.session.query(UsersMedia).filter(and_(UsersMedia.user_id==self.user_id, UsersMedia.media_id==data['id'])).first()
        self.assertEqual(um.play_pos, data['pos'])

    def test_media_state_delete(self):
        data = {'id': 4}
        resp = self.req_sess.delete(self.fullpath+'/media/state', headers={'token': self.token}, params=data)
        um = self.session.query(UsersMedia).filter(and_(UsersMedia.user_id==self.user_id, UsersMedia.media_id==data['id'])).first()
        self.assertFalse(um.watched)
        self.assertFalse(um.play_pos)

    def tearDown(self):
        self.session.remove()
