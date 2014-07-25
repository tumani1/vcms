# coding: utf-8
import yaml
import requests
import zerorpc
import unittest
import datetime
from settings import CONFIG_PATH
from os.path import join

from tests.create_test_user import create
from models import Base, Topics, SessionToken, UsersTopics, Users, CDN, Extras, ExtrasTopics
from utils.connection import db_connect, create_session, get_session


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


# ###################################################################################
# class TopicInfoTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.engine = db_connect().connect()
#         self.session = create_session(bind=self.engine, expire_on_commit=False)
#
#
#         self.cl = zerorpc.Client(timeout=3000)
#         self.cl.connect("tcp://127.0.0.1:4242")
#
#         self.user_id = 1
#         self.session_token = SessionToken.generate_token(self.user_id, session=self.session)
#
#
#     def test_echo(self):
#         topic = "test"
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "info",
#             "api_format": "json",
#             "x_token": self.session_token[1],
#             "http_method": "get",
#             "query_params": {
#                 "name": topic,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         temp = {
#             'name': 'test',
#             'title': 'test',
#             'title_orig': None,
#             'description': 'test test',
#             'releasedate': 1388534400.0,
#             'type': 'news',
#             'relation': {
#                 'subscribed': False,
#                 'liked': 0,
#             }
#         }
#
#         self.assertDictEqual(temp, resp)
#
#
#     def tearDown(self):
#         self.cl.close()
#         self.session.close()
#         self.engine.close()
#

###################################################################################
class TopicLikeTestCase(unittest.TestCase):

    def setUp(self):
        with open(join(CONFIG_PATH, 'node_service.yaml')) as file:
            conf = yaml.safe_load(file)
        self.h, self.p = conf['rest_ws_serv']['host'], conf['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)
        self.req_sess = requests.Session()
        db_sess = get_session()
        create(db_sess)

        self.user_id = 1



    def test_echo_get(self):
        resp = self.req_sess.get(self.fullpath + '/topics/like', data={'name': 'test'})
        temp = {'liked': 0}
        self.assertDictEqual(temp, resp.content)


#     def test_echo_post(self):
#         topic = "test1"
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "like",
#             "api_format": "json",
#             "x_token": self.session_token[1],
#             "http_method": "post",
#             "query_params": {
#                 "name": topic,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         self.assertEqual(resp, None)
#
#         user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()
#
#         topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
#         self.assertNotEqual(topic.liked, None)
#
#
#     def test_echo_delete(self):
#         topic = "test2"
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "like",
#             "api_format": "json",
#             "x_token": self.session_token[1],
#             "http_method": "delete",
#             "query_params": {
#                 "name": topic,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         self.assertEqual(resp, None)
#
#         user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()
#
#         topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
#         self.assertEqual(topic.liked, None)
#
#
#     def tearDown(self):
#         self.cl.close()
#         self.session.close()
#         self.engine.close()
#
#
# ###################################################################################
# class TopicSubscribeTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.engine = db_connect().connect()
#         self.session = create_session(bind=self.engine, expire_on_commit=False)
#
#         self.cl = zerorpc.Client(timeout=300)
#         self.cl.connect("tcp://127.0.0.1:4242")
#
#         self.user_id = 1
#         self.session_token = SessionToken.generate_token(self.user_id, session=self.session)
#
#
#     def test_echo_get(self):
#         topic = "test"
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "subscribe",
#             "api_format": "json",
#             "x_token": self.session_token[1],
#             "http_method": "get",
#             "query_params": {
#                 "name": topic,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         temp = {'subscribed': 0}
#
#         self.assertDictEqual(temp, resp)
#
#
#     def test_echo_post(self):
#         topic = "test2"
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "subscribe",
#             "api_format": "json",
#             "x_token": self.session_token[1],
#             "http_method": "post",
#             "query_params": {
#                 "name": topic,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         self.assertEqual(resp, None)
#
#         user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()
#
#         topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
#         self.assertNotEqual(topic.subscribed, None)
#
#
#     def test_echo_delete(self):
#         topic = "test1"
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "subscribe",
#             "api_format": "json",
#             "x_token": self.session_token[1],
#             "http_method": "delete",
#             "query_params": {
#                 "name": topic,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         self.assertEqual(resp, None)
#
#         user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()
#
#         topic = UsersTopics.get_user_topic(user=user, name=topic, session=self.session).first()
#         self.assertEqual(topic.subscribed, None)
#
#
#     def tearDown(self):
#         self.cl.close()
#         self.session.close()
#         self.engine.close()
#
#
# ###################################################################################
# class TopicExtrasTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.engine = db_connect().connect()
#         self.session = create_session(bind=self.engine, expire_on_commit=False)
#
#         self.cl = zerorpc.Client(timeout=3000)
#         self.cl.connect("tcp://127.0.0.1:4242")
#
#
#     def test_echo(self):
#         topic = 'test'
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "extras",
#             "api_format": "json",
#             "http_method": "get",
#             "query_params": {
#                 "name": topic,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#
#         temp = [
#             {
#                 'description': 'test test',
#                 'created': 1388534400.0,
#                 'title': 'test',
#                 'title_orig': 'test',
#                 'location': 'russia',
#                 'type': 'v',
#                 'id': 1
#             }, {
#                 'description': 'test1 test',
#                 'created': 1388534400.0,
#                 'title': 'test1',
#                 'title_orig': 'test1',
#                 'location': 'russia',
#                 'type': 'v',
#                 'id': 2
#             }
#         ]
#
#         self.assertListEqual(temp, resp)
#
#     def tearDown(self):
#         self.cl.close()
#         self.session.close()
#         self.engine.close()
#
#
# ###################################################################################
# class TopicListTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.engine = db_connect().connect()
#         self.session = create_session(bind=self.engine, expire_on_commit=False)
#
#         self.cl = zerorpc.Client(timeout=300)
#         self.cl.connect("tcp://127.0.0.1:4242")
#
#
#     def test_echo(self):
#         topic = 'news'
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "list",
#             "api_format": "json",
#             "http_method": "get",
#             "query_params": {
#                 "type": topic,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         self.assertEqual(len(resp), 2)
#
#         temp = [
#             {
#                 'description': 'test test',
#                 'title': 'test1',
#                 'releasedate': 1388534400.0,
#                 'relation': {},
#                 'title_orig': None,
#                 'type': 'news',
#                 'name': 'test1'
#             }, {
#                 'description': 'test test',
#                 'title': 'test',
#                 'releasedate': 1388534400.0,
#                 'relation': {},
#                 'title_orig': None,
#                 'type': 'news',
#                 'name': 'test'
#             }
#         ]
#         self.assertListEqual(temp, resp)
#
#
#     def tearDown(self):
#         self.cl.close()
#         self.session.close()
#         self.engine.close()
#
#
# ###################################################################################
# class TopicValuesTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.engine = db_connect().connect()
#         self.session = create_session(bind=self.engine, expire_on_commit=False)
#
#         self.cl = zerorpc.Client(timeout=300)
#         self.cl.connect("tcp://127.0.0.1:4242")
#
#     def test_echo(self):
#         topic = "test"
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "values",
#             "api_format": "json",
#             "http_method": "get",
#             "query_params": {
#                 "name": topic,
#                 "scheme_name": "t",
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         temp = []
#
#         self.assertEqual(temp, resp)
#
#     def tearDown(self):
#         self.cl.close()
#         self.session.close()
#         self.engine.close()
#
#
# ###################################################################################
# class TopicMediaTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.engine = db_connect().connect()
#         self.session = create_session(bind=self.engine, expire_on_commit=False)
#
#         self.cl = zerorpc.Client(timeout=300)
#         self.cl.connect("tcp://127.0.0.1:4242")
#
#
#     def test_echo(self):
#         topic = "test"
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "media",
#             "api_format": "json",
#             "http_method": "get",
#             "query_params": {
#                 "name": topic,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         temp = []
#
#         self.assertEqual(temp, resp)
#
#     def tearDown(self):
#         self.cl.close()
#         self.session.close()
#         self.engine.close()
#
#
# ###################################################################################
# class TopicPersonsTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.engine = db_connect().connect()
#         self.session = create_session(bind=self.engine, expire_on_commit=False)
#
#         self.cl = zerorpc.Client(timeout=300)
#         self.cl.connect("tcp://127.0.0.1:4242")
#
#
#     def test_echo(self):
#         topic = "test"
#         IPC_pack = {
#             "api_group": "topics",
#             "api_method": "persons",
#             "api_format": "json",
#             "http_method": "get",
#             "query_params": {
#                 "name": topic,
#             }
#         }
#
#         resp = self.cl.route(IPC_pack)
#         temp = []
#
#         self.assertEqual(temp, resp)
#
#     def tearDown(self):
#         self.cl.close()
#         self.session.close()
#         self.engine.close()
