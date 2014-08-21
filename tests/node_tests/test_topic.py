# coding: utf-8
import requests
import unittest

from tests.constants import NODE
from models import Base, UsersTopics, Users
from utils.connection import db_connect, create_session
from tests.fixtures import create, create_topic, create_user_topic, create_cdn, \
    create_extras, create_topic_extras, create_topic_values, create_scheme


def setUpModule():
    engine = db_connect().connect()
    # engine.execute("drop schema public cascade; create schema public;")
    session = create_session(bind=engine)

    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)
    create_topic(session)
    create_user_topic(session)
    create_cdn(session)
    create_scheme(session)
    create_extras(session)
    create_topic_extras(session)
    create_topic_values(session)

    engine.close()


def tearDownModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")


################################################################################
class TopicInfoTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()

        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'})
        self.token = resp.json()['token']

    def test_echo(self):
        topic = 'test'
        resp = self.req_sess.get(self.fullpath + '/topics/{0}/info'.format(topic), headers={'token': self.token}, params={})

        temp = {
            u'name': u'test',
            u'title': u'test',
            u'title_orig': None,
            u'description': u'test test',
            u'releasedate': 1388534400,
            u'type': u'news',
            u'relation': {
                u'subscribed': False,
                u'liked': 0,
            }
        }

        self.assertDictEqual(temp, resp.json())

    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()


################################################################################
class TopicLikeTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()
        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'})
        self.token = resp.json()['token']

    def test_echo_get(self):
        topic = 'test'
        resp = self.req_sess.get(self.fullpath + '/topics/{0}/like'.format(topic), headers={'token': self.token}, params={})
        temp = {
            'liked': 0
        }
        self.assertDictEqual(temp, resp.json())

    def test_echo_post(self):
        topic = "test1"
        self.req_sess.post(self.fullpath + '/topics/{0}/like'.format(topic), headers={'token': self.token}, data={})

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertNotEqual(topic.liked, None)

    def test_echo_delete(self):
        topic = "test2"
        self.req_sess.delete(self.fullpath + '/topics/{0}/like'.format(topic), headers={'token': self.token}, params={})

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertEqual(topic.liked, None)

    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()


# ##############################################################################
class TopicSubscribeTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()
        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'})
        self.token = resp.json()['token']

    def test_echo_get(self):
        topic = "test"
        resp = self.req_sess.get(self.fullpath + '/topics/{0}/subscribe'.format(topic), headers={'token': self.token}, params={})

        temp = {'subscribed': 0}

        self.assertDictEqual(temp, resp.json())

    def test_echo_post(self):
        topic = "test2"
        resp = self.req_sess.post(self.fullpath + '/topics/{0}/subscribe'.format(topic), headers={'token': self.token}, data={})

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertNotEqual(topic.subscribed, None)

    def test_echo_delete(self):
        topic = "test1"
        resp = self.req_sess.delete(self.fullpath + '/topics/{0}/subscribe'.format(topic), headers={'token': self.token}, params={})

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertEqual(topic.subscribed, None)

    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()


################################################################################
class TopicExtrasTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'})
        self.token = resp.json()['token']

    def test_echo(self):
        topic = 'test'
        resp = self.req_sess.get(self.fullpath + '/topics/{0}/extras'.format(topic), headers={'token': self.token}, params={})

        temp = [
            {
                'description': 'test test',
                'created': 1388534400,
                'title': 'test',
                'title_orig': 'test',
                'location': 'russia',
                'type': 'v',
                'id': 1
            }, {
                'description': 'test1 test',
                'created': 1388534400,
                'title': 'test1',
                'title_orig': 'test1',
                'location': 'russia',
                'type': 'v',
                'id': 2
            }
        ]

        self.assertListEqual(temp, resp.json())

    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()


################################################################################
class TopicListTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()
        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'})
        self.token = resp.json()['token']

    def test_echo(self):
        resp = self.req_sess.get(self.fullpath + '/topics/list', headers={'token': self.token}, params={'type': 'news'})

        temp = [
            {
                'description': 'test test',
                'title': 'test1',
                'releasedate': 1388534400,
                'relation': {'liked': 0, 'subscribed': True},
                'title_orig': None,
                'type': 'news',
                'name': 'test1'
            }, {
                'description': 'test test',
                'title': 'test',
                'releasedate': 1388534400,
                'relation': {'liked': 0, 'subscribed': False},
                'title_orig': None,
                'type': 'news',
                'name': 'test'
            }
        ]
        self.assertListEqual(temp, resp.json())

    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()


################################################################################
class TopicValuesTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()
        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'})
        self.token = resp.json()['token']

    def test_echo(self):
        topic = "test"
        resp = self.req_sess.get(self.fullpath + '/topics/{0}/values'.format(topic), headers={'token': self.token}, params={'scheme_name': 't'})

        temp = []

        self.assertEqual(temp, resp.json())

    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()


################################################################################
class TopicMediaTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()
        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'})
        self.token = resp.json()['token']


    def test_echo(self):
        topic = "test"
        resp = self.req_sess.get(self.fullpath + '/topics/{0}/media'.format(topic), headers={'token': self.token}, params={})

        temp = []

        self.assertListEqual(temp, resp.json())

    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()


################################################################################
class TopicPersonsTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()
        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'})
        self.token = resp.json()['token']

    def test_echo(self):
        topic = "test"
        resp = self.req_sess.get(self.fullpath + '/topics/{0}/persons'.format(topic), headers={'token': self.token}, params={})

        temp = []

        self.assertListEqual(temp, resp.json())

    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()
