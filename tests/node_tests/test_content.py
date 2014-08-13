import unittest
import requests
from models import Base
from settings import NODE
from tests.fixtures import create, create_content
from utils.connection import db_connect, create_session


HOST = NODE['rest_ws_serv']['host']
PORT = NODE['rest_ws_serv']['port']
URL = 'http://{}:{}'.format(HOST, PORT)


def setUpModule():
    engine = db_connect().connect()
    engine.execute("drop schema public cascade; create schema public;")
    session = create_session(bind=engine)

    # Create table
    Base.metadata.create_all(bind=engine)

    create_content(session)

    engine.close()


class ContentInfoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = db_connect().connect()
        cls.session = create_session(bind=cls.engine, expire_on_commit=False)

        cls.h, cls.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        cls.fullpath = 'http://{}:{}'.format(cls.h, cls.p)

        cls.req_sess = requests.Session()

    def test_get_info(self):
        resp = ContentInfoTestCase.req_sess.get(ContentInfoTestCase.fullpath + '/content/1/info')
        result = {
            u'text': u'test',
            u'id': 1,
            u'title': None
        }
        self.assertDictEqual(resp.json(), result)

    @classmethod
    def tearDownClass(cls):
        ContentInfoTestCase.session.close()
        ContentInfoTestCase.engine.close()
        ContentInfoTestCase.req_sess.close()


class ContentListTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = db_connect().connect()
        cls.session = create_session(bind=cls.engine, expire_on_commit=False)

        cls.h, cls.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        cls.fullpath = 'http://{}:{}'.format(cls.h, cls.p)

        cls.req_sess = requests.Session()

    def test_get_list(self):
        resp = ContentInfoTestCase.req_sess.get(ContentInfoTestCase.fullpath + '/content/list')
        result = {
            u'text': u'test',
            u'id': 1,
            u'title': None
        }
        self.assertDictEqual(resp.json()[0], result)

    @classmethod
    def tearDownClass(cls):
        ContentInfoTestCase.session.close()
        ContentInfoTestCase.engine.close()
        ContentInfoTestCase.req_sess.close()

