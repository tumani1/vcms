import json
import unittest
import requests
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base
from tests.fixtures import (create,  create_items, create_cdn, create_extras,
     create_items_extras, create_cart, create_cart_log, create_variants, create_variants_extras, create_items_carts,
     create_items_objects, create_payments)
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
    create_cart_log(session)
    create_items(session)
    create_cdn(session)
    create_extras(session)
    create_items_extras(session)
    create_variants(session)
    create_variants_extras(session)
    create_items_carts(session)
    create_items_objects(session)
    create_payments(session)


def tearDownModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")


class CartStatTestCase(unittest.TestCase):
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

    def test_cart_stat_get(self):

        resp = self.req_sess.get(self.fullpath+'/eshop/cart/stat', headers={'token': self.token}, params={})

        data = {
            'items_cnt': 1,
            'total_cnt': 1,
            'cost': 10,
            'id': 1
        }

        self.assertDictEqual(resp.json(), data)


class CartItemsTestCase(unittest.TestCase):
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

    def test_cart_items_get(self):

        resp = self.req_sess.get(self.fullpath+'/eshop/cart/items', headers={'token': self.token}, params={})

        list_extras = []

        extras = {
            'id': 1,
            'description': 'test test',
            'created': 1388534400.0,
            'location': 'russia',
            'title': 'test',
            'type': 'Video',
            'title_orig': 'test'
        }

        list_extras.append(extras)

        mShopItem  = {
            'name': 'item1',
            'description': 'item_test',
            'instock': False,
            'id': 1,
            'is_digital': True,
            'price': None,
            'price_old': None,
            'extras': list_extras,
            'relation': {}
        }
        list_data = []
        data = {
            'id': 1,
            'cart_id': 1,
            'added': None,
            'cnt': 1,
            'cost': 10.0,
            'price': 10.0,
            'variant_id': 1,
            'item': mShopItem

        }
        list_data.append(data)

        self.assertListEqual(resp.json(), list_data)


class CartsTestCase(unittest.TestCase):
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

        cls.list_extras = []
        cls.extras = {
            'id': 1,
            'description': 'test test',
            'created': 1388534400.0,
            'location': 'russia',
            'title': 'test',
            'type': 'Video',
            'title_orig': 'test'
        }
        cls.list_extras.append(cls.extras)
        cls.mShopItem  = {
            'name': 'item1',
            'description': 'item_test',
            'instock': False,
            'id': 1,
            'is_digital': True,
            'price': None,
            'price_old': None,
            'extras': cls.list_extras,
            'relation': {}
        }

        cls.mShopCartItem = {
            'id': 1,
            'cart_id': 1,
            'added': None,
            'cnt': 1,
            'cost': 10.0,
            'price': 10.0,
            'item': cls.mShopItem,
            'variant_id': 1
        }
        cls.mShopCartLog = {
            'id': 1,
            'cart_id': 1,
            'time': None,
            'status': None,
            'comment': 'cart'
        }

        cls.mShopCart = {
            'id': 1,
            'created': 1391284800.0,
            'status': 'active',
            'payed': None,
            'cost': 10.0,
            'items': cls.mShopCartItem,
            'log': cls.mShopCartLog,
            'items_cnt': 1
        }
        cls.list_mShopCart = []

        cls.list_mShopCart.append(cls.mShopCart)

    @classmethod
    def tearDown(cls):
        cls.session.close()
        cls.req_sess.close()

    def test_carts_list_get(self):
        resp = self.req_sess.get(self.fullpath+'/eshop/carts/list', headers={'token': self.token}, params={})

        data = {
            'cnt': 1,
            'total_cnt': 1,
            'items': self.list_mShopCart
        }

        self.assertDictEqual(resp.json(), data)

    def test_carts_info_get_by_id(self):
        resp = self.req_sess.get(self.fullpath+'/eshop/carts/{id}/info'.format(id=1), headers={'token': self.token}, params={})

        self.assertDictEqual(resp.json(), self.mShopCart)

    def test_carts_items_get_by_id(self):
        resp = self.req_sess.get(self.fullpath+'/eshop/carts/{id}/items'.format(id=1), headers={'token': self.token}, params={})

        data = []
        data.append(self.mShopCartItem)

        self.assertListEqual(resp.json(), data)

    def test_carts_log_get_by_id(self):

        resp = self.req_sess.get(self.fullpath+'/eshop/carts/{id}/log'.format(id=1), headers={'token': self.token}, params={})

        data = []

        data.append(self.mShopCartLog)

        self.assertListEqual(resp.json(), data)



