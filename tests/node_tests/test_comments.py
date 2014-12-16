# coding: utf-8
import unittest
import json
import requests
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker, scoped_session

from models import Base, Comments, UsersComments, SessionToken
from settings import DATABASE
from utils.connection import db_connect, create_session, mongo_connect
from tests.fixtures import create_media_units, create_topic, create, create_media, create_persons, create_comments
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
        self.token = SessionToken.generate_token(self.user_id, session=self.session)[1]

    def test_comments_info(self):
        data = {}
        id = 1
        resp = self.req_sess.get(self.fullpath+'/comments/{0}/info'.format(id), headers={'x-token': self.token}, params=data)
        temp = {
            'text': u'Тест',
            'relation': {},
            'id': 1,
            'user': {'firstname': 'Test1', 'lastname': 'Test1', 'relation': 'u', 'is_online': True, 'person_id': 1,'id': 1
            }
        }
        self.assertDictEqual(json.loads(resp.content), temp)

    def test_comments_list(self):
        data = {'obj_type': 'm', 'obj_id': 1, 'with_obj': True}
        resp = self.req_sess.get(self.fullpath+'/comments/list', headers={'x-token': self.token}, params=data)
        temp = [
            {
                'text': u'Тест',
                'object':
                    {
                        'rating': 0.0,
                        'description': 'test_desc1',
                        'title': 'media1',
                        'locations': [],
                        'id': 1,
                        'releasedate': None,
                        'duration': None,
                        'title_orig': 'test_media1',
                        'units': [
                            {
                                'topic':
                                    {
                                        'name': 'test1',
                                        'title': 'test1',
                                        'releasedate': 1388534400.0,
                                        'relation':
                                            {
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
                    },
                'relation': {},
                'id': 1,
                'user': {'firstname': 'Test1', 'lastname': 'Test1', 'relation': 'u', 'is_online': True, 'person_id': 1, 'id': 1}}]
        self.assertListEqual(json.loads(resp.content), temp)

    def test_comments_create(self):
        data = {'text': 'test_create', 'obj_type': 'mu', 'obj_id': 2}
        resp = self.req_sess.post(self.fullpath+'/comments/create', headers={'x-token': self.token}, params=data)
        self.session.close()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        new_com = self.session.query(Comments).all()[-1]
        self.assertTrue(new_com)
        self.assertEqual(new_com.obj_type, data['obj_type'])
        self.assertEqual(new_com.obj_id, data['obj_id'])
        self.assertEqual(new_com.text, data['text'])

    def test_comments_like_put(self):
        data = {}
        id = 2
        resp = self.req_sess.put(self.fullpath+'/comments/{0}/like'.format(id), headers={'x-token': self.token}, params=data)
        self.session.close()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        new_like = self.session.query(UsersComments).filter(and_(UsersComments.user_id == self.user_id, UsersComments.comment_id == id)).first()
        self.assertTrue(new_like)
        self.assertTrue(new_like.liked)

    def test_comments_like_delete(self):
        data = {}
        id = 3
        user_com = self.session.query(UsersComments).filter(and_(UsersComments.user_id == self.user_id, UsersComments.comment_id == id)).first()
        self.assertTrue(user_com.liked)
        resp = self.req_sess.delete(self.fullpath+'/comments/{0}/like'.format(id), headers={'x-token': self.token}, params=data)
        self.session.close()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        user_com = self.session.query(UsersComments).filter(and_(UsersComments.user_id == self.user_id, UsersComments.comment_id == id)).first()
        self.assertTrue(user_com)
        self.assertFalse(user_com.liked)

    def test_comments_reply(self):
        data = {'text': 'reply_test'}
        id = 1
        resp = self.req_sess.post(self.fullpath+'/comments/{0}/reply'.format(id), headers={'x-token': self.token}, params=data)
        self.session.close()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        reply_com = self.session.query(Comments).all()[-1]
        self.assertTrue(reply_com)
        self.assertEqual(reply_com.parent_id, id)
        self.assertEqual(reply_com.text, data['text'])


    def tearDown(self):
        self.session.remove()
