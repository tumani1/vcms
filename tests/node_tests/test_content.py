import unittest
import requests
from models import Base
from settings import NODE
from tests.fixtures import create
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

    create(session)

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
        self.assertEqual(resp.json(), 1)


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
        self.assertEqual(resp.json(), 1)