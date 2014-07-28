# coding: utf-8
import unittest
from models import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from utils.connection import db_connect, create_session
from tests.api_tests.fixtures import create_media_units, create_topic, create
from settings import NODE
import requests
import json


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


def tearDownModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")


class MediaUnitsTestCase(unittest.TestCase):

    def setUp(self):
        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)
        self.req_sess = requests.Session()
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.user_id = 1
        token_str = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'}).content
        self.token = json.loads(token_str)['token']

    def test_info(self):
        data = {'id': 2}
        resp = self.req_sess.get(self.fullpath+'/mediaunits/info', headers={'token': self.token}, params=data)
        temp = '{"releasedate":1325361600,"next":3,"title_orig":2,"description":"test2","title":"mu2",' \
               '"enddate":1391198400,"prev":1,"id":2,"relation":{"watched":1388520000},"batch":"batch1"}'
        self.assertEqual(resp.content, temp)

    def test_next(self):
        data = {'id': 2}
        resp = self.req_sess.get(self.fullpath+'/mediaunits/next', headers={'token': self.token}, params=data)
        temp = '{"releasedate":1356984000,"next":null,"title_orig":3,"description":"test3","title":"mu3",' \
               '"enddate":1391198400,"prev":2,"id":3,"relation":{},"batch":"batch1"}'
        self.assertEqual(resp.content, temp)

    def test_prev(self):
        data = {'id': 3}
        resp = self.req_sess.get(self.fullpath+'/mediaunits/prev', headers={'token': self.token}, params=data)
        temp = '{"releasedate":1325361600,"next":3,"title_orig":2,"description":"test2",' \
               '"title":"mu2","enddate":1391198400,"prev":1,"id":2,"relation":{"watched":1388520000},"batch":"batch1"}'
        self.assertEqual(resp.content, temp)

    def test_list(self):
        data = {'text': 'mu1'}
        resp = self.req_sess.get(self.fullpath+'/mediaunits/list', headers={'token': self.token}, params=data)
        temp = '[{"releasedate":1293829200,"next":2,"title_orig":1,"description":"test1","title":"mu1",' \
               '"enddate":1391198400,"prev":null,"id":1,"relation":{"watched":1388520000},"batch":"batch1"}]'
        self.assertEqual(resp.content, temp)

    def tearDown(self):
        self.session.remove()