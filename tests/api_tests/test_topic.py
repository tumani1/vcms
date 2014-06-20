# coding: utf-8

import zerorpc
import unittest
import datetime

from tests.create_test_user import create
from models import Base, Topics, SessionToken, UsersTopics, Users
from db_engine import db, db_connect, create_session


@db
def create_topic(session):
    topic1 = Topics(name="test", title="test", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0), status="a", type="news")
    topic2 = Topics(name="test1", title="test1", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0), status="a", type="news")
    topic3 = Topics(name="test2", title="test2", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0), status="a", type="news")

    session.add_all([topic1, topic2, topic3])
    session.commit()


@db
def create_user_topic(session):
    ut1 = UsersTopics(user_id=1, topic_name="test")
    ut2 = UsersTopics(user_id=1, topic_name="test1", subscribed=datetime.datetime(2014,1,1,0,0,0))
    ut3 = UsersTopics(user_id=1, topic_name="test2", liked=datetime.datetime(2014,1,1,0,0,0))

    session.add_all([ut1, ut2, ut3])
    session.commit()


def setUpModule():
    engine = db_connect().connect()

    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create()
    create_topic()
    create_user_topic()

    engine.close()


def tearDownModule():
    pass


###################################################################################
class TopicInfoTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)


        self.cl = zerorpc.Client(timeout=3000)
        self.cl.connect("tcp://127.0.0.1:4242")

        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)


    def test_echo(self):
        topic = "test"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "info",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "get",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        temp = {
            'name': 'test',
            'title': 'test',
            'title_orig': None,
            'description': 'test test',
            'releasedate': 1388520000.0,
            'type': 'news',
            'relation': {
                'subscribed': False,
                'liked': 0,
            }
        }

        self.assertDictEqual(temp, resp)


    def tearDown(self):
        self.cl.close()
        self.session.close()
        self.engine.close()


###################################################################################
class TopicLikeTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.cl = zerorpc.Client(timeout=300)
        self.cl.connect("tcp://127.0.0.1:4242")

        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)


    def test_echo_get(self):
        topic = "test"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "like",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "get",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        temp = {'liked': 0}

        self.assertDictEqual(temp, resp)


    def test_echo_post(self):
        topic = "test1"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "like",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "post",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        self.assertEqual(resp, None)

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertNotEqual(topic.liked, None)


    def test_echo_delete(self):
        topic = "test2"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "like",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "delete",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        self.assertEqual(resp, None)

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertEqual(topic.liked, None)


    def tearDown(self):
        self.cl.close()
        self.session.close()
        self.engine.close()


###################################################################################
class TopicSubscribeTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.cl = zerorpc.Client(timeout=300)
        self.cl.connect("tcp://127.0.0.1:4242")

        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)


    def test_echo_get(self):
        topic = "test"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "subscribe",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "get",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        temp = {'subscribed': 0}

        self.assertDictEqual(temp, resp)


    def test_echo_post(self):
        topic = "test2"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "subscribe",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "post",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        self.assertEqual(resp, None)

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertNotEqual(topic.subscribed, None)


    def test_echo_delete(self):
        topic = "test1"
        IPC_pack = {
            "api_group": "topics",
            "api_method": "subscribe",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "delete",
            "query_params": {
                "name": topic,
            }
        }

        resp = self.cl.route(IPC_pack)
        self.assertEqual(resp, None)

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
        self.assertEqual(topic.subscribed, None)


    def tearDown(self):
        self.cl.close()
        self.session.close()
        self.engine.close()


# ###################################################################################
# class TopicExtrasTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.cl = zerorpc.Client(timeout=300)
#         self.cl.connect("tcp://127.0.0.1:4242")
#         self.topic = create_topic()
#
#
#     def test_echo(self):
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "extras",
#             "api_format": "json",
#             "http_method": "get",
#             "query_params": {
#                 "name": self.topic.name,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         temp = {}
#
#         self.assertEqual(temp, resp)
#
#     def tearDown(self):
#         self.cl.close()
#
#
# ###################################################################################
# class TopicListTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.cl = zerorpc.Client(timeout=300)
#         self.cl.connect("tcp://127.0.0.1:4242")
#         self.topic = create_topic()
#
#
#     def test_echo(self):
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "list",
#             "api_format": "json",
#             "http_method": "get",
#             "query_params": {
#                 "name": self.topic.name,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         temp = {}
#
#         self.assertEqual(temp, resp)
#
#     def tearDown(self):
#         self.cl.close()
#
#
# ###################################################################################
# class TopicValuesTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.cl = zerorpc.Client(timeout=300)
#         self.cl.connect("tcp://127.0.0.1:4242")
#         self.topic = create_topic()
#
#
#     def test_echo(self):
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "values",
#             "api_format": "json",
#             "http_method": "get",
#             "query_params": {
#                 "name": self.topic.name,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         temp = {}
#
#         self.assertEqual(temp, resp)
#
#     def tearDown(self):
#         self.cl.close()
#
#
# ###################################################################################
# class TopicMediaTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.cl = zerorpc.Client(timeout=300)
#         self.cl.connect("tcp://127.0.0.1:4242")
#         self.topic = create_topic()
#
#
#     def test_echo(self):
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "media",
#             "api_format": "json",
#             "http_method": "get",
#             "query_params": {
#                 "name": self.topic.name,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         temp = {}
#
#         self.assertEqual(temp, resp)
#
#     def tearDown(self):
#         self.cl.close()
#
#
# ###################################################################################
# class TopicPersonsTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.cl = zerorpc.Client(timeout=300)
#         self.cl.connect("tcp://127.0.0.1:4242")
#         self.topic = create_topic()
#
#
#     def test_echo(self):
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "persons",
#             "api_format": "json",
#             "http_method": "get",
#             "query_params": {
#                 "name": self.topic.name,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         temp = {}
#
#         self.assertEqual(temp, resp)
#
#     def tearDown(self):
#         self.cl.close()
