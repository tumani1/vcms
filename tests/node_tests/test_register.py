# coding: utf-8
import unittest
from models import Base, Users
from sqlalchemy.orm import sessionmaker, scoped_session
from utils.connection import db_connect, create_session
from tests.fixtures import create
from settings import NODE
import requests


def setUpModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")
    session = create_session(bind=engine)

    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)


def tearDownModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")


class RegisterTestCase(unittest.TestCase):

    def setUp(self):
        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)
        self.req_sess = requests.Session()
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def test_auth_register(self):
        data = {
            'firstname': 'Petr',
            'lastname': 'Petrov',
            'email': 'petrov@mail.ru',
            'pswd1': 'test',
            'pswd2': 'test',
            'city_id': 1
        }
        resp = self.req_sess.post(self.fullpath+'/auth/register', params=data)
        self.session.close()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        new_user = self.session.query(Users).all()[-1]
        self.assertEqual(data['firstname'], new_user.firstname)
        self.assertEqual(data['lastname'], new_user.lastname)
        self.assertEqual(data['email'], new_user.email)
        self.assertEqual(data['city_id'], new_user.city_id)

    def tearDown(self):
        self.session.remove()