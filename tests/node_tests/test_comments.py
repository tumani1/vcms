# coding: utf-8
import unittest
from models import Base, Comments, UsersComments
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker, scoped_session
from utils.connection import db_connect, create_session
from tests.fixtures import create_media_units, create_topic, create, create_media, create_persons, create_comments
from settings import NODE
import requests
import json


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
    create_comments(session)


def tearDownModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")


class CommentsTestCase(unittest.TestCase):

    def setUp(self):
        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)
        self.req_sess = requests.Session()
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.user_id = 1
        token_str = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'}).content
        self.token = json.loads(token_str)['token']

    def test_comments_info(self):
        data = {'id': 1}
        resp = self.req_sess.get(self.fullpath+'/comments/info', headers={'token': self.token}, params=data)
        temp = {
            u'text': u'Test',
            u'object': None,
            u'relation': {},
            u'id': 1,
            u'user': {
                u'firstname': u'Test1',
                u'lastname': u'Test1',
                u'relation': u'u',
                u'is_online': False,
                u'person_id': 1,
                u'id': 1
            }
        }
        self.assertDictEqual(resp.json(), temp)

    def test_comments_list(self):
        data = {'obj_type': 'm', 'obj_id': 1, 'with_obj': True}
        resp = self.req_sess.get(self.fullpath+'/comments/list', headers={'token': self.token}, params=data)
        temp = {
            u'text': u'Test',
            u'object': {u'description': u'test_desc1', u'title': u'media1', u'locations': [], u'releasedate': None, u'title_orig': u'test_media1', u'duration': None, u'relation': {u'watched': 1356984000, u'liked': 1388520000, u'pos': 50}, u'id': 1},
            u'relation': {},
            u'id': 1,
            u'user': {u'firstname': u'Test1', u'lastname': u'Test1', u'relation': u'u', u'is_online': False, u'person_id': 1, u'id': 1}
        }
        self.assertDictEqual(resp.json()[0], temp)

    def test_comments_create(self):
        data = {'text': 'test_create', 'obj_type': 'mu', 'obj_id': 2}
        resp = self.req_sess.post(self.fullpath+'/comments/create', headers={'token': self.token}, params=data)
        self.session.close()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        new_com = self.session.query(Comments).all()[-1]
        self.assertTrue(new_com)
        self.assertEqual(new_com.obj_type, data['obj_type'])
        self.assertEqual(new_com.obj_id, data['obj_id'])
        self.assertEqual(new_com.text, data['text'])

    def test_comments_like_put(self):
        data = {'id': 2}
        resp = self.req_sess.put(self.fullpath+'/comments/like', headers={'token': self.token}, params=data)
        self.session.close()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        new_like = self.session.query(UsersComments).filter(and_(UsersComments.user_id == self.user_id, UsersComments.comment_id == data['id'])).first()
        self.assertTrue(new_like)
        self.assertTrue(new_like.liked)

    def test_comments_like_delete(self):
        data = {'id': 3}
        user_com = self.session.query(UsersComments).filter(and_(UsersComments.user_id == self.user_id, UsersComments.comment_id == data['id'])).first()
        self.assertTrue(user_com.liked)
        resp = self.req_sess.delete(self.fullpath+'/comments/like', headers={'token': self.token}, params=data)
        self.session.close()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        user_com = self.session.query(UsersComments).filter(and_(UsersComments.user_id == self.user_id, UsersComments.comment_id == data['id'])).first()
        self.assertTrue(user_com)
        self.assertFalse(user_com.liked)

    def test_comments_reply(self):
        data = {'id': 1, 'text': 'reply_test'}
        resp = self.req_sess.post(self.fullpath+'/comments/reply', headers={'token': self.token}, params=data)
        self.session.close()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        reply_com = self.session.query(Comments).all()[-1]
        self.assertTrue(reply_com)
        self.assertEqual(reply_com.parent_id, data['id'])
        self.assertEqual(reply_com.text, data['text'])


    def tearDown(self):
        self.session.remove()
