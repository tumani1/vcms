# coding: utf-8
import zerorpc
import unittest
from models import Base, SessionToken, Comments
from sqlalchemy.orm import sessionmaker, scoped_session
from utils.connection import db_connect, create_session
from tests.constants import ZERORPC_SERVICE_URI
from tests.fixtures import create_media_units, create_topic, create, create_media, create_persons, create_comments


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


class ObjCommentsTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.cl = zerorpc.Client(timeout=3000)
        self.cl.connect(ZERORPC_SERVICE_URI, )
        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)

    def test_obj_comments_list(self):
        IPC_pack = {'api_group': 'obj_comments',
                'api_method': 'list',
                'http_method': 'get',
                'api_format': 'json',
                'x_token': self.session_token[1],
                'query_params': {'type': 'm', 'id': 1}
        }
        temp = [{
                    'text': 'Тест',
                    'object': None,
                    'relation': {},
                    'id': 1,
                    'user': {'firstname': 'Test1', 'lastname': 'Test1', 'relation': 'u', 'is_online': True, 'person_id': 1, 'id': 1}
                }]
        resp = self.cl.route(IPC_pack)
        self.assertListEqual(resp, temp)

    def test_obj_comments_create(self):
        IPC_pack = {'api_group': 'obj_comments',
                'api_method': 'create',
                'http_method': 'post',
                'api_format': 'json',
                'x_token': self.session_token[1],
                'query_params': {'text': 'test_create', 'type': 'mu', 'id': 2}
        }
        resp = self.cl.route(IPC_pack)
        new_com = self.session.query(Comments).all()[-1]
        self.assertTrue(new_com)
        self.assertEqual(new_com.obj_type, IPC_pack['query_params']['type'])
        self.assertEqual(new_com.obj_id, IPC_pack['query_params']['id'])
        self.assertEqual(new_com.text, IPC_pack['query_params']['text'])

    def tearDown(self):
        self.session.remove()