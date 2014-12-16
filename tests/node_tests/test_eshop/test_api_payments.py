import json
import unittest
import requests
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base
from tests.fixtures import create_cart, create_payments, create
from utils.connection import db_connect, create_session
from tests.constants import NODE


def setUpModule():
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")
    session = create_session(bind=engine)
    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)
    create_cart(session)
    create_payments(session)


def tearDownModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")


class PaymentsListTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.h, cls.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        cls.fullpath = 'http://{}:{}'.format(cls.h, cls.p)
        cls.req_sess = requests.Session()
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))

        token_str = cls.req_sess.post(cls.fullpath+'/auth/login', data={'login': 'test1@test.ru', 'password': 'Test1'}).content
        cls.token = json.loads(token_str)['token']
        cls.engine = db_connect()


    @classmethod
    def tearDown(cls):
        cls.session.close()
        cls.req_sess.close()

    def test_payments_list_get(self):

        resp = self.req_sess.get(self.fullpath+'/eshop/payments/list', headers={'token': self.token}, params={})


        data = {
            'cnt': 1,
            'total_cnt': 1,
            'items': ''
        }

        mShopPayment = {
            'id': 1,
            'cart_id': 1,
            'created': 1391284800.0,
            'status': 'active',
            'cost': 10.0,
            'payed': None,
            'pay_system': None
        }
        list_mShopPayment = []
        list_mShopPayment.append(mShopPayment)

        data['items'] = list_mShopPayment

        self.assertDictEqual(resp.json(), data)
