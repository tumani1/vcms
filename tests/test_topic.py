# coding: utf-8

import zerorpc
import unittest
import datetime

from create_test_user import create
from models import Base, Topics, SessionToken
from db_engine import db, db_connect, create_session


engine = db_connect()
session = create_session(bind=engine, expire_on_commit=False)

@db
def create_topic(session):
    topic1 = Topics(name="test", title="test", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0), status="a", type="news")
    topic2 = Topics(name="test1", title="test1", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0), status="a", type="news")
    topic3 = Topics(name="test2", title="test2", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0), status="a", type="news")

    session.add_all([topic1, topic2, topic3])
    session.commit()


@db
def create_topic(session):
    topic1 = Topics(name="test", title="test", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0), status="a", type="news")
    topic2 = Topics(name="test1", title="test1", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0), status="a", type="news")
    topic3 = Topics(name="test2", title="test2", description="test test", releasedate=datetime.datetime(2014,1,1,0,0,0), status="a", type="news")

    session.add_all([topic1, topic2, topic3])
    session.commit()


def setUpModule():
    engine.execute("drop schema public cascade; create schema public;")

    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create()
    create_topic()




def tearDownModule():
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")



# ###################################################################################
# class TopicInfoTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.cl = zerorpc.Client(timeout=3000)
#         self.cl.connect("tcp://127.0.0.1:4242")
#         self.topic = "test"
#
#         self.user_id = 1
#         self.session_token = SessionToken.generate_token(self.user_id, session=session)
#
#
#     def test_echo(self):
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "info",
#             "api_format": "json",
#             "x_token": self.session_token[1],
#             "http_method": "get",
#             "query_params": {
#                 "name": self.topic,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         temp = {
#             'name': 'test',
#             'title': 'test',
#             'title_orig': None,
#             'description': 'test test',
#             'releasedate': 1388520000.0,
#             'type': 'news',
#             'relation': {
#                 'subscribed': False,
#                 'liked': 0,
#             }
#         }
#
#         self.assertDictEqual(temp, resp)
#
#     def tearDown(self):
#         self.cl.close()


###################################################################################
class TopicLikeTestCase(unittest.TestCase):

    def setUp(self):
        self.cl = zerorpc.Client(timeout=300)
        self.cl.connect("tcp://127.0.0.1:4242")

        self.topic = create_topic()

        self.user_id = create()
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)


    def test_echo_get(self):
        IPC_pack = {
            "api_group": "topics",
            "api_method": "like",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "get",
            "query_params": {
                "name": self.topic.name,
            }
        }

        resp = self.cl.route(IPC_pack)
        temp = {}

        self.assertEqual(temp, resp)


    def test_echo_post(self):
        IPC_pack = {
            "api_group": "topics",
            "api_method": "like",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "post",
            "query_params": {
                "name": self.topic.name,
            }
        }

        resp = self.cl.route(IPC_pack)
        temp = {}

        self.assertEqual(temp, resp)


    def test_echo_delete(self):
        IPC_pack = {
            "api_group": "topics",
            "api_method": "like",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "delete",
            "query_params": {
                "name": self.topic.name,
            }
        }

        resp = self.cl.route(IPC_pack)
        temp = {}

        self.assertEqual(temp, resp)


    def tearDown(self):
        self.cl.close()


# ###################################################################################
# class TopicSubscribeTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.cl = zerorpc.Client(timeout=300)
#         self.cl.connect("tcp://127.0.0.1:4242")
#
#         self.topic = create_topic()
#
#         self.user_id = create()
#         self.session_token = SessionToken.generate_token(self.user_id, session=self.session)
#
#
#
#     def test_echo_get(self):
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "subscribe",
#             "api_format": "json",
#             "x_token": self.session_token[1],
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
#
#     def test_echo_post(self):
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "subscribe",
#             "api_format": "json",
#             "x_token": self.session_token[1],
#             "http_method": "post",
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
#
#     def test_echo_delete(self):
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "subscribe",
#             "api_format": "json",
#             "x_token": self.session_token[1],
#             "http_method": "delete",
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
#
#     def tearDown(self):
#         self.cl.close()
#
#
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
