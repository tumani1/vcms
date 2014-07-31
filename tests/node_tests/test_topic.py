# coding: utf-8
import json

import requests
import unittest
import datetime
from settings import NODE

from tests.create_test_user import create
from models import Base, Topics, UsersTopics, Users, CDN, Extras, ExtrasTopics
from utils.connection import db_connect, create_session


def create_topic(session):
    list_topics = [
        Topics(name="test", title="test", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0,0), status="a", type="news"),
        Topics(name="test1", title="test1", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0,0), status="a", type="news"),
        Topics(name="test2", title="test2", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0,0), status="a", type="show"),
    ]

    session.add_all(list_topics)
    session.commit()


def create_user_topic(session):
    list_uts = [
        UsersTopics(user_id=1, topic_name="test"),
        UsersTopics(user_id=1, topic_name="test1", subscribed=datetime.datetime(2014,1,1,0,0,0,0)),
        UsersTopics(user_id=1, topic_name="test2", liked=datetime.datetime(2014,1,1,0,0,0,0)),
    ]

    session.add_all(list_uts)
    session.commit()


def create_cdn(session):
    list_cdn = [
        CDN(name="cdn1", description="test", has_mobile=False, has_auth=False, url="ya.ru", location_regxp="", cdn_type=""),
        CDN(name="cdn2", description="test", has_mobile=False, has_auth=True, url="google.com", location_regxp="", cdn_type=""),
    ]

    session.add_all(list_cdn)
    session.commit()


def create_extras(session):
    list_extras = [
        Extras(cdn_name='cdn1', type="v", location="russia", description="test test", title="test", title_orig="test", created=datetime.datetime(2014,1,1,0,0,0,0)),
        Extras(cdn_name='cdn1', type="v", location="russia", description="test1 test", title="test1", title_orig="test1", created=datetime.datetime(2014,1,1,0,0,0,0)),
        Extras(cdn_name='cdn1', type="a", location="russia", description="test2 test", title="test2", title_orig="test2", created=datetime.datetime(2014,1,1,0,0,0,0)),
        Extras(cdn_name='cdn1', type="a", location="russia", description="test test", title="test", title_orig="test", created=datetime.datetime(2014,1,1,0,0,0,0)),
        Extras(cdn_name='cdn2', type="v", location="russia", description="test1 test", title="test1", title_orig="test1", created=datetime.datetime(2014,1,1,0,0,0,0)),
        Extras(cdn_name='cdn2', type="v", location="russia", description="test2 test", title="test2", title_orig="test2", created=datetime.datetime(2014,1,1,0,0,0,0)),
    ]

    session.add_all(list_extras)
    session.commit()


def create_topic_extras(session):
    list_te = [
        ExtrasTopics(extras_id=1, topic_name="test"),
        ExtrasTopics(extras_id=1, topic_name="test1"),
        ExtrasTopics(extras_id=1, topic_name="test2"),
        ExtrasTopics(extras_id=2, topic_name="test"),
        ExtrasTopics(extras_id=3, topic_name="test1"),
        ExtrasTopics(extras_id=4, topic_name="test2"),
    ]


    session.add_all(list_te)
    session.commit()


def setUpModule():
    engine = db_connect().connect()
    engine.execute("drop schema public cascade; create schema public;")
    session = create_session(bind=engine)

    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)
    create_topic(session)
    create_user_topic(session)
    create_cdn(session)
    create_extras(session)
    create_topic_extras(session)

    engine.close()


def tearDownModule():
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")


###################################################################################
class TopicInfoTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()

        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test'})
        self.token = resp.json()['token']

    def test_echo(self):
        topic = "test"
        resp = self.req_sess.get(self.fullpath + '/topics/info', headers={'token': self.token}, params={'name': topic})

        temp = {
            u'name': u'test',
            u'title': u'test',
            u'title_orig': None,
            u'description': u'test test',
            u'releasedate': 1388520000,
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



###################################################################################
class TopicLikeTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()
        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test'})
        self.token = resp.json()['token']



    def test_echo_get(self):
        resp = self.req_sess.get(self.fullpath + '/topics/like', headers={'token': self.token}, params={'name': 'test'})
        temp = {
            'liked': 0
        }
        self.assertDictEqual(temp, resp.json())


    def test_echo_post(self):
        topic = "test1"
        self.req_sess.post(self.fullpath + '/topics/like', headers={'token': self.token}, data={'name': topic})

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertNotEqual(topic.liked, None)


    def test_echo_delete(self):
        topic = "test2"
        self.req_sess.delete(self.fullpath + '/topics/like', headers={'token': self.token}, params={'name': topic})

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertEqual(topic.liked, None)


    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()


# ###################################################################################
class TopicSubscribeTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()
        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test'})
        self.token = resp.json()['token']


    def test_echo_get(self):
        topic = "test"
        resp = self.req_sess.get(self.fullpath + '/topics/subscribe', headers={'token': self.token}, params={'name': topic})

        temp = {'subscribed': 0}

        self.assertDictEqual(temp, resp.json())


    def test_echo_post(self):
        topic = "test2"
        resp = self.req_sess.post(self.fullpath + '/topics/subscribe', headers={'token': self.token}, data={'name': topic})

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertNotEqual(topic.subscribed, None)


    def test_echo_delete(self):
        topic = "test1"
        resp = self.req_sess.delete(self.fullpath + '/topics/subscribe', headers={'token': self.token}, params={'name': topic})

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertEqual(topic.subscribed, None)


    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()


###################################################################################
class TopicExtrasTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test'})
        self.token = resp.json()['token']


    def test_echo(self):
        topic = 'test'
        resp = self.req_sess.get(self.fullpath + '/topics/extras', headers={'token': self.token}, params={'name': topic})

        temp = [
            {
                'description': 'test test',
                'created': 1388520000,
                'title': 'test',
                'title_orig': 'test',
                'location': 'russia',
                'type': 'v',
                'id': 1
            }, {
                'description': 'test1 test',
                'created': 1388520000,
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


###################################################################################
class TopicListTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()
        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test'})
        self.token = resp.json()['token']

    def test_echo(self):
        topic = 'news'
        resp = self.req_sess.get(self.fullpath + '/topics/list', headers={'token': self.token}, params={'name': topic})

        temp = [
            {
                'description': 'test test',
                'title': 'test1',
                'releasedate': 1388534400.0,
                'relation': {},
                'title_orig': None,
                'type': 'news',
                'name': 'test1'
            }, {
                'description': 'test test',
                'title': 'test',
                'releasedate': 1388534400.0,
                'relation': {},
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


###################################################################################
class TopicValuesTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()
        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test'})
        self.token = resp.json()['token']

    def test_echo(self):
        topic = "test"
        resp = self.req_sess.get(self.fullpath + '/topics/values', headers={'token': self.token}, params={'name': topic, 'scheme_name': 't'})

        temp = []

        self.assertEqual(temp, resp.json())

    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()


##################################################################################
class TopicMediaTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()
        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test'})
        self.token = resp.json()['token']


    def test_echo(self):
        topic = "test"
        resp = self.req_sess.get(self.fullpath + '/topics/media', headers={'token': self.token}, params={'name': topic})

        temp = []

        self.assertListEqual(temp, resp.json())

    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()


##################################################################################
class TopicPersonsTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()
        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test'})
        self.token = resp.json()['token']


    def test_echo(self):
        topic = "test"
        resp = self.req_sess.get(self.fullpath + '/topics/persons', headers={'token': self.token}, params={'name': topic})

        temp = []

        self.assertListEqual(temp, resp.json())

    def tearDown(self):
        self.session.close()
        self.engine.close()
        self.req_sess.close()
