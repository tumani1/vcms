import json
import unittest
import requests
from sqlalchemy import and_
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base, ItemsCarts
from tests.fixtures import (create,  create_items, create_cdn, create_extras,
     create_items_extras, create_cart, create_variants, create_variants_extras, create_items_carts,
     create_items_objects,  create_categories, create_items_categories, create_categories_extras)
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
    create_categories(session)
    create_items(session)
    create_items_categories(session)
    create_cart(session)
    create_cdn(session)
    create_extras(session)
    create_categories_extras(session)
    create_items_extras(session)
    create_variants(session)
    create_variants_extras(session)
    create_items_objects(session)
    create_items_carts(session)


def tearDownModule():
    engine = db_connect()
    #engine.execute("drop schema public cascade; create schema public;")


class ItemsInfoTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.h, cls.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        cls.fullpath = 'http://{}:{}'.format(cls.h, cls.p)
        cls.req_sess = requests.Session()
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))
        token_str = cls.req_sess.post(cls.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'}).content
        cls.token = json.loads(token_str)['token']
        cls.engine = db_connect()

    @classmethod
    def tearDown(cls):
        cls.session.close()
        cls.req_sess.close()

    def test_items_info_get(self):
        list_extras = []
        resp = self.req_sess.get(self.fullpath+'/eshop/items/{id}/info'.format(id=1), headers={'token': self.token}, params={})
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
        data = {
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

        self.assertDictEqual(resp.json(), data)


class ItemsVariantsTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.h, cls.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        cls.fullpath = 'http://{}:{}'.format(cls.h, cls.p)
        cls.req_sess = requests.Session()
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))
        token_str = cls.req_sess.post(cls.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'}).content
        cls.token = json.loads(token_str)['token']
        cls.engine = db_connect()

    @classmethod
    def tearDown(cls):
        cls.session.close()
        cls.req_sess.close()

    def test_items_variants_get(self):
        resp = self.req_sess.get(self.fullpath+'/eshop/items/{id}/variants'.format(id=1), headers={'token': self.token}, params={})
        list_extras = []
        extras = {
            'id': 2,
            'description': 'test1 test',
            'created': 1388534400.0,
            'location': 'russia',
            'title': 'test1',
            'type': 'Video',
            'title_orig': 'test1'
        }
        list_extras.append(extras)

        data_list = []

        data = {
            'id': 1,
            'item_id': 1,
            'name': 'variants1',
            'description': 'variants1',
            'price': 1.0,
            'price_old': 1.0,
            'extras': list_extras,
            'values': [],
            'available_cnt': 1
        }

        data_list.append(data)

        self.assertListEqual(resp.json(), data_list)


class ItemsBookTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.h, cls.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        cls.fullpath = 'http://{}:{}'.format(cls.h, cls.p)
        cls.req_sess = requests.Session()
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))
        token_str = cls.req_sess.post(cls.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'}).content
        cls.token = json.loads(token_str)['token']
        cls.engine = db_connect()

    @classmethod
    def tearDown(cls):
        cls.session.close()
        cls.req_sess.close()

    def test_items_book_post(self):

        self.req_sess.post(self.fullpath+'/eshop/items/{id}/book'.format(id=1), headers={'token': self.token})

        item_cart = self.session.query(ItemsCarts).filter(and_(ItemsCarts.carts_id == 1, ItemsCarts.variant_id == 1)).first()

        self.assertEqual(item_cart.cost, 2.0)

    def test_items_book_delete(self):

        self.req_sess.post(self.fullpath+'/eshop/items/{id}/book'.format(id=1), headers={'token': self.token})

        self.req_sess.delete(self.fullpath+'/eshop/items/{id}/book'.format(id=1), headers={'token': self.token})

        item_cart = self.session.query(ItemsCarts).filter(and_(ItemsCarts.carts_id == 1, ItemsCarts.variant_id == 1)).first()

        self.assertEqual(item_cart.cost, 1.0)


class ItemsListTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.h, cls.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        cls.fullpath = 'http://{}:{}'.format(cls.h, cls.p)
        cls.req_sess = requests.Session()
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))
        token_str = cls.req_sess.post(cls.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'}).content
        cls.token = json.loads(token_str)['token']
        cls.engine = db_connect()

        cls.list_extras1 = []
        cls.list_extras2 = []
        cls.extras1 = {
            'id': 1,
            'description': 'test test',
            'created': 1388534400.0,
            'location': 'russia',
            'title': 'test',
            'type': 'Video',
            'title_orig': 'test'
        }
        cls.extras2 = {
            'id': 2,
            'description': 'test1 test',
            'created': 1388534400.0,
            'location': 'russia',
            'title': 'test1',
            'type': 'Video',
            'title_orig': 'test1'
        }

        cls.list_extras1.append(cls.extras1)

        cls.mShopItem1  = {
            'name': 'item1',
            'description': 'item_test',
            'instock': False,
            'id': 1,
            'is_digital': True,
            'price': None,
            'price_old': None,
            'extras': cls.list_extras1,
            'relation': {}
        }

        cls.list_extras2.append(cls.extras2)

        cls.mShopItem2  = {
            'name': 'item2',
            'description': 'item2_test',
            'instock': True,
            'id': 2,
            'is_digital': True,
            'price': None,
            'price_old': None,
            'extras': cls.list_extras2,
            'relation': {}
        }

        cls.mShopItem3  = {
            'name': 'item3',
            'description': 'item3_test',
            'instock': False,
            'id': 3,
            'is_digital': True,
            'price': None,
            'price_old': None,
            'extras': [],
            'relation': {}
        }

        cls.mShopItem4  = {
            'name': 'item4',
            'description': 'item4_test',
            'instock': True,
            'id': 4,
            'is_digital': True,
            'price': None,
            'price_old': None,
            'extras': [],
            'relation': {}
        }

        cls.list_mShopItem = []

    @classmethod
    def tearDown(cls):
        cls.session.close()
        cls.req_sess.close()

    def test_items_list_get(self):
        resp = self.req_sess.get(self.fullpath+'/eshop/items/list', headers={'token': self.token}, params={})

        self.list_mShopItem.append(self.mShopItem1)
        self.list_mShopItem.append(self.mShopItem2)
        self.list_mShopItem.append(self.mShopItem4)
        self.list_mShopItem.append(self.mShopItem3)

        data = {
            'cnt': 4,
            'total_cnt': 4,
            'items': self.list_mShopItem
        }

        self.assertDictEqual(resp.json(), data)

    def test_items_limit_list_get(self):

        resp = self.req_sess.get(self.fullpath+'/eshop/items/list', headers={'token': self.token}, params={'limit': '3'})

        self.list_mShopItem.append(self.mShopItem1)
        self.list_mShopItem.append(self.mShopItem2)
        self.list_mShopItem.append(self.mShopItem4)

        data = {
            'cnt': 3,
            'total_cnt': 4,
            'items': self.list_mShopItem
        }

        self.assertDictEqual(resp.json(), data)

    def test_items_list_get_by_name(self):
        resp = self.req_sess.get(self.fullpath+'/eshop/items/list', headers={'token': self.token}, params={'name': 'item1'})

        self.list_mShopItem.append(self.mShopItem1)

        data = {
            'cnt': 1,
            'total_cnt': 1,
            'items': self.list_mShopItem
        }

        self.assertDictEqual(resp.json(), data)

    def test_items_list_get_by_id(self):
        resp = self.req_sess.get(self.fullpath+'/eshop/items/list', headers={'token': self.token}, params={'id': 2})

        self.list_mShopItem.append(self.mShopItem2)

        data = {
            'cnt': 1,
            'total_cnt': 1,
            'items': self.list_mShopItem
        }

        self.assertDictEqual(resp.json(), data)

    def test_items_list_get_by_instock_true(self):
        resp = self.req_sess.get(self.fullpath+'/eshop/items/list', headers={'token': self.token}, params={'instock': 1})

        self.list_mShopItem.append(self.mShopItem2)
        self.list_mShopItem.append(self.mShopItem4)

        data = {
            'cnt': 2,
            'total_cnt': 2,
            'items': self.list_mShopItem
        }

        self.assertDictEqual(resp.json(), data)

    def test_items_list_get_by_instock_false(self):
        resp = self.req_sess.get(self.fullpath+'/eshop/items/list', headers={'token': self.token}, params={'instock': 0})

        self.list_mShopItem.append(self.mShopItem1)
        self.list_mShopItem.append(self.mShopItem3)

        data = {
            'cnt': 2,
            'total_cnt': 2,
            'items': self.list_mShopItem
        }

        self.assertDictEqual(resp.json(), data)

    def test_items_list_get_by_cat_id(self):
        resp = self.req_sess.get(self.fullpath+'/eshop/items/list', headers={'token': self.token}, params={'cat': 1})

        self.list_mShopItem.append(self.mShopItem1)

        data = {
            'cnt': 1,
            'total_cnt': 1,
            'items': self.list_mShopItem
        }

        self.assertDictEqual(resp.json(), data)


class ItemsObjectsTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.h, cls.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        cls.fullpath = 'http://{}:{}'.format(cls.h, cls.p)
        cls.req_sess = requests.Session()
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))
        token_str = cls.req_sess.post(cls.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'}).content
        cls.token = json.loads(token_str)['token']
        cls.engine = db_connect()

    @classmethod
    def tearDown(cls):
        cls.session.close()
        cls.req_sess.close()

    def test_items_objects_get(self):

        resp = self.req_sess.get(self.fullpath+'/eshop/items/{id}/objects'.format(id=1), headers={'token': self.token}, params={})

        self.assertDictEqual({}, {})


class ItemsExtrasTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.h, cls.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        cls.fullpath = 'http://{}:{}'.format(cls.h, cls.p)
        cls.req_sess = requests.Session()
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))
        token_str = cls.req_sess.post(cls.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'}).content
        cls.token = json.loads(token_str)['token']
        cls.engine = db_connect()

    @classmethod
    def tearDown(cls):
        cls.session.close()
        cls.req_sess.close()

    def test_items_extras_get(self):
        resp = self.req_sess.get(self.fullpath+'/eshop/items/{id}/extras'.format(id=1), headers={'token': self.token}, params={})
        list_mExtra = []

        mExtra = {
            'id': 1,
            'created': 1388534400.0,
            'description': 'test test',
            'title': 'test',
            'location': 'russia',
            'type': 'Video',
            'title': 'test',
            'title_orig': 'test'
        }

        list_mExtra.append(mExtra)

        self.assertListEqual(resp.json(), list_mExtra)

    def test_items_extras_get_by_variant(self):

        resp = self.req_sess.get(self.fullpath+'/eshop/items/{id}/extras'.format(id=1), headers={'token': self.token}, params={'variant': 1})

        list_mExtra = []

        mExtra = {
            'id': 2,
            'created': 1388534400.0,
            'description': 'test1 test',
            'title': 'test1',
            'location': 'russia',
            'type': 'Video',
            'title': 'test1',
            'title_orig': 'test1'
        }

        list_mExtra.append(mExtra)

        self.assertListEqual(resp.json(), list_mExtra)


