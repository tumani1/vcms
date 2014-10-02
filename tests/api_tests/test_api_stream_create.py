# coding: utf-8
import zerorpc
import unittest

from models import Base
from models.tokens import SessionToken
from models.media import Media
from models.mongo import Stream, constant as stream_const
from models.users import constants as user_const, Users
from tests.constants import ZERORPC_SERVICE_URI
from tests.fixtures import create_one_media
from tests.create_test_user import create
from utils.common import datetime_to_unixtime, get_or_create
from utils.connection import db_connect, create_session, mongo_connect


def setUpModule():
    engine = db_connect()
    mongo_connect()
    engine.execute("drop schema public cascade; create schema public;")
    Base.metadata.create_all(bind=engine)
    session = create_session(bind=engine)
    create_one_media(session=session)


def tearDownModule():
    engine = db_connect()
    Stream.objects().delete()
    engine.execute("drop schema public cascade; create schema public;")


class StreamCreateTestCase(unittest.TestCase):
    def setUp(self):
        engine = db_connect()
        self.session = create_session(bind=engine)
        self.client = zerorpc.Client(timeout=3000)
        self.client.connect(ZERORPC_SERVICE_URI)
        Stream.objects().delete()
        self.auth_user, create = get_or_create(session=self.session, model=Users,
                                               filter={'firstname': 'Test1', 'lastname': 'Test1'},
                                               create={'firstname': 'Test1', 'lastname': 'Test1', 'password': 'Test', 'email': 'test1@test.ru'})
        if create:
            self.session.commit()
        self.ipc_pack = {
            'api_method': '',
            'api_type': 'get',
            'x_token': SessionToken.generate_token(user_id=self.auth_user.id, session=self.session)[1],
            'query_params': {}
        }

    def test_user_send_friend(self):
        user = create(session=self.session, usuff=2, cisuff=2)
        # User send offer for friendship
        self.ipc_pack['api_method'] = '/users/{0}/friendship'.format(user.id)
        self.ipc_pack['api_type'] = 'post'
        self.client.route(self.ipc_pack)
        try:
            stream_obj = Stream.objects().get(type=stream_const.APP_STREAM_TYPE_USER_A)
        except:
            stream_obj = None
        self.assertIsNotNone(stream_obj)
        self.ipc_pack['api_method'] = '/stream/{0}/info'.format(stream_obj.id)
        self.ipc_pack['api_type'] = 'get'
        response = self.client.route(self.ipc_pack)
        m_stream = {
            'created': datetime_to_unixtime(stream_obj.created),
            'text': stream_obj.text,
            'object': {
                'lastname': user.lastname,
                'relation': user_const.APP_USERSRELS_TYPE_SEND_TO,
                'id': user.id,
                'firstname': user.firstname,
                'is_online': False
            },
            'attach': {},
            'relation': {'liked': None},
            'user': {
                'lastname': self.auth_user.lastname,
                'relation': user_const.APP_USERSRELS_TYPE_UNDEF,
                'id': self.auth_user.id,
                'firstname': self.auth_user.firstname,
                'is_online': True,
            },
            'type': stream_const.APP_STREAM_TYPE_USER_A,
            'id': stream_obj.id
        }
        self.assertDictEqual(m_stream, response)

    def test_user_friend(self):
        user = create(session=self.session, usuff=3, cisuff=3)
        # User is friends
        self.ipc_pack['api_method'] = '/users/{0}/friendship'.format(user.id)
        self.ipc_pack['api_type'] = 'post'
        self.client.route(self.ipc_pack)
        self.client.route(self.ipc_pack)
        try:
            stream_obj = Stream.objects().get(type=stream_const.APP_STREAM_TYPE_USER_F)
        except:
            stream_obj = None
        self.assertIsNotNone(stream_obj)

        self.ipc_pack['api_method'] = '/stream/{0}/info'.format(stream_obj.id)
        self.ipc_pack['api_type'] = 'get'
        response = self.client.route(self.ipc_pack)
        m_stream = {
            'created': datetime_to_unixtime(stream_obj.created),
            'text': stream_obj.text,
            'object': {
                'lastname': user.lastname,
                'relation': user_const.APP_USERSRELS_TYPE_FRIEND,
                'id': user.id,
                'firstname': user.firstname,
                'is_online': False
            },
            'attach': {},
            'relation': {'liked': None},
            'user': {
                'lastname': self.auth_user.lastname,
                'relation': user_const.APP_USERSRELS_TYPE_UNDEF,
                'id': self.auth_user.id,
                'firstname': self.auth_user.firstname,
                'is_online': True,
            },
            'type': stream_const.APP_STREAM_TYPE_USER_F,
            'id': stream_obj.id
        }
        self.assertDictEqual(m_stream, response)

    def test_media_like(self):
        media = self.session.query(Media).filter_by(title='Test').first()
        self.ipc_pack['api_method'] = '/media/{0}/like'.format(media.id)
        self.ipc_pack['api_type'] = 'post'
        self.client.route(self.ipc_pack)
        users_media = media.users_media.filter_by(users=self.auth_user).first()
        try:
            stream_obj = Stream.objects().get(type=stream_const.APP_STREAM_TYPE_MEDIA_L)
        except:
            stream_obj = None
        self.assertIsNotNone(stream_obj)
        self.ipc_pack['api_method'] = '/stream/{0}/info'.format(stream_obj.id)
        self.ipc_pack['api_type'] = 'get'
        response = self.client.route(self.ipc_pack)
        m_stream = {
            'created': datetime_to_unixtime(stream_obj.created),
            'text': stream_obj.text,
            'id': stream_obj.id,
            'attach': {},
            'type': stream_const.APP_STREAM_TYPE_MEDIA_L,
            'relation': {'liked': None},
            'object': {
                'id': media.id,
                'title': media.title,
                'title_orig': media.title_orig,
                'description': media.description,
                'releasedate': datetime_to_unixtime(media.release_date),
                'duration': media.duration,
                'relation': {
                    'liked': datetime_to_unixtime(users_media.liked),
                },
                'locations': [],
            },
            'user': {
                'lastname': self.auth_user.lastname,
                'relation': user_const.APP_USERSRELS_TYPE_UNDEF,
                'id': self.auth_user.id,
                'firstname': self.auth_user.firstname,
                'is_online': True,
            },
        }
        self.assertDictEqual(m_stream, response)

    def test_media_comments(self):
        pass

    def test_person_subscribe(self):
        pass

    def test_person_media(self):
        pass

    def tearDown(self):
        self.session.close()
        self.client.close()