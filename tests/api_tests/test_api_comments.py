# coding: utf-8
import zerorpc
import unittest
from models import Base, SessionToken, Comments, UsersComments
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import and_
from utils.connection import db_connect, create_session

from tests.constants import ZERORPC_SERVICE_URI
from tests.fixtures import create_media_units, create_topic, create, create_media, create_persons, create_comments


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
    create_persons(session)
    create_media(session)
    create_comments(session)


def tearDownModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")


class CommentsTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.cl = zerorpc.Client(timeout=3000)
        self.cl.connect(ZERORPC_SERVICE_URI, )
        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)

    def test_comments_info(self):
        id = 1
        IPC_pack = {
                    'api_method': '/comments/%s/info' % (id),
                    'api_type': 'get',
                    'query_params': {
                        'x_token': self.session_token[1]
                    }
        }
        temp = {
            'text': 'Тест',
            'object': None,
            'relation': {},
            'id': 1,
            'user': {'firstname': 'Test1', 'lastname': 'Test1', 'relation': 'u', 'is_online': True, 'person_id': 1,'id': 1
            }
        }
        resp = self.cl.route(IPC_pack)
        self.assertDictEqual(resp, temp)

    def test_comments_list(self):
        IPC_pack = {
                'api_method': '/comments/list',
                'api_type': 'get',
                'query_params': {
                    'obj_type': 'm',
                    'obj_id': 1,
                    'with_obj': True,
                    'x_token': self.session_token[1]}
        }
        temp = [{
                    'text': 'Тест',
                    'object': {'description': 'test_desc1', 'title': 'media1', 'locations': [], 'releasedate': None, 'title_orig': 'test_media1', 'duration': None, 'relation': {'watched': 1356998400.0, 'liked': 1388534400.0, 'pos': 50}, 'id': 1},
                    'relation': {},
                    'id': 1,
                    'user': {'firstname': 'Test1', 'lastname': 'Test1', 'relation': 'u', 'is_online': True, 'person_id': 1,'id': 1}
                }]
        resp = self.cl.route(IPC_pack)
        self.assertListEqual(resp, temp)

    def test_comments_create(self):
        IPC_pack = {
                'api_method': '/comments/create',
                'api_type': 'post',
                'query_params': {
                    'text': 'test_create',
                    'obj_type': 'mu',
                    'obj_id': 2,
                    'x_token': self.session_token[1]}
        }
        resp = self.cl.route(IPC_pack)
        new_com = self.session.query(Comments).all()[-1]
        self.assertTrue(new_com)
        self.assertEqual(new_com.obj_type, IPC_pack['query_params']['obj_type'])
        self.assertEqual(new_com.obj_id, IPC_pack['query_params']['obj_id'])
        self.assertEqual(new_com.text, IPC_pack['query_params']['text'])

    def test_comments_like_put(self):
        id = 2
        IPC_pack = {
                'api_method': '/comments/%s/like'  % (id),
                'api_type': 'put',
                'query_params': {
                    'x_token': self.session_token[1],
                }
        }
        resp = self.cl.route(IPC_pack)
        new_like = self.session.query(UsersComments).filter(and_(UsersComments.user_id == self.user_id, UsersComments.comment_id == id)).first()
        self.assertTrue(new_like)
        self.assertTrue(new_like.liked)

    def test_comments_like_delete(self):
        id = 3
        IPC_pack = {
                'api_method': '/comments/%s/like'  % (id),
                'api_type': 'delete',
                'query_params': {
                    'x_token': self.session_token[1]
                }
        }
        user_com = self.session.query(UsersComments).filter(and_(UsersComments.user_id == self.user_id, UsersComments.comment_id == id)).first()
        self.assertTrue(user_com.liked)
        resp = self.cl.route(IPC_pack)
        self.session.close()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        user_com = self.session.query(UsersComments).filter(and_(UsersComments.user_id == self.user_id, UsersComments.comment_id == id)).first()
        self.assertTrue(user_com)
        self.assertFalse(user_com.liked)

    def test_comments_reply(self):
        id = 1
        IPC_pack = {
                'api_method': '/comments/%s/reply'  % (id),
                'api_type': 'post',
                'query_params': {
                    'text': 'reply_test',
                    'x_token': self.session_token[1]
                }
        }
        resp = self.cl.route(IPC_pack)
        reply_com = self.session.query(Comments).all()[-1]
        self.assertTrue(reply_com)
        self.assertEqual(reply_com.parent_id, id)
        self.assertEqual(reply_com.text, IPC_pack['query_params']['text'])

    def tearDown(self):
        self.session.remove()