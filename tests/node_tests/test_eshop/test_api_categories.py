import json
import unittest
import requests
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base
from tests.fixtures import (create, create_categories, create_items, create_items_categories, create_cdn, create_extras,
     create_categories_extras, create_items_extras)
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
    create_cdn(session)
    create_extras(session)
    create_categories_extras(session)
    create_items_extras(session)


def tearDownModule():
    engine = db_connect()
    #engine.execute("drop schema public cascade; create schema public;")


class CategoriesInfoTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.h, cls.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        cls.fullpath = 'http://{}:{}'.format(cls.h, cls.p)
        cls.req_sess = requests.Session()
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))


        cls.engine = db_connect()

    @classmethod
    def tearDown(cls):
        cls.session.close()
        cls.req_sess.close()

    def test_info_get(self):
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
        data = {
            'items_cnt': 1,
            'instock_cnt': 0,
            'name': 'category1',
            'description': 'category_test',
            'extras': list_extras
        }

        resp = self.req_sess.get(self.fullpath+'/eshop/categories/{id}/info'.format(id=1), params={})
        self.assertDictEqual(resp.json(), data)


class CategoriesExtrasTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.h, cls.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        cls.fullpath = 'http://{}:{}'.format(cls.h, cls.p)
        cls.req_sess = requests.Session()
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))

        cls.engine = db_connect()

    @classmethod
    def tearDown(cls):
        cls.session.close()
        cls.req_sess.close()

    def test_extras_get(self):
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

        resp = self.req_sess.get(self.fullpath+'/eshop/categories/{id}/extras'.format(id=1), params={})

        self.assertListEqual(resp.json(), list_extras)


class CategoriesItemsTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.h, cls.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        cls.fullpath = 'http://{}:{}'.format(cls.h, cls.p)
        cls.req_sess = requests.Session()
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))

        cls.engine = db_connect()

    @classmethod
    def tearDown(cls):
        cls.session.close()
        cls.req_sess.close()

    def test_items_get(self):
        resp = self.req_sess.get(self.fullpath+'/eshop/categories/{id}/items'.format(id=1), params={})

        list_mShopItem = []
        list_extras1 = []
        extras1 = {
            'id': 1,
            'description': 'test test',
            'created': 1388534400.0,
            'location': 'russia',
            'title': 'test',
            'type': 'Video',
            'title_orig': 'test'
        }

        list_extras1.append(extras1)
        mShopItem1  = {
            'name': 'item1',
            'description': 'item_test',
            'instock': False,
            'id': 1,
            'is_digital': True,
            'price': None,
            'price_old': None,
            'extras': list_extras1,
            'relation': {}
        }

        list_mShopItem.append(mShopItem1)

        data = {
            'cnt': 1,
            'total_cnt': 1,
            'items': list_mShopItem
        }

        self.assertDictEqual(resp.json(), data)


class CategoriesListTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.h, cls.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        cls.fullpath = 'http://{}:{}'.format(cls.h, cls.p)
        cls.req_sess = requests.Session()
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))

        cls.engine = db_connect()

    @classmethod
    def tearDown(cls):
        cls.session.close()
        cls.req_sess.close()

    def test_list_get_has_items_true(self):
        resp = self.req_sess.get(self.fullpath+'/eshop/categories/list', params={'has_items': 1})
        list_category = []

        category1 = {
            'id': 2,
            'name': 'category2'
        }
        category2 = {
            'id': 1,
            'name': 'category1'
        }
        category3 = {
            'id': 4,
            'name': 'category4'
        }

        list_category.append(category1)
        list_category.append(category3)
        list_category.append(category2)
        self.assertListEqual(resp.json(), list_category)

    def test_list_get_has_items_false(self):
        category = {
            'id': 3,
            'name': 'category3'
        }

        list_category = []

        list_category.append(category)
        resp = self.req_sess.get(self.fullpath+'/eshop/categories/list', params={'has_items': 0})
        self.assertListEqual(resp.json(), list_category)

    def test_list_get_instock_true(self):

        list_category = []

        category = {
            'id': 2,
            'name': 'category2'
        }
        category2 = {
            'id': 4,
            'name': 'category4'
        }

        list_category.append(category)
        list_category.append(category2)

        resp = self.req_sess.get(self.fullpath+'/eshop/categories/list', params={'instock': 1})

        self.assertListEqual(resp.json(), list_category)

    def test_list_get_instock_false(self):
        list_category = []

        category = {
            'id': 1,
            'name': 'category1'
        }
        category2 = {
            'id': 4,
            'name': 'category4'
        }

        list_category.append(category2)
        list_category.append(category)

        resp = self.req_sess.get(self.fullpath+'/eshop/categories/list', params={'instock': 0})

        self.assertListEqual(resp.json(), list_category)

    def test_list_get_sort_by_name(self):
        list_category = []

        category1 = {
            'id': 1,
            'name': 'category1'
        }
        category2 = {
            'id': 2,
            'name': 'category2'
        }
        category3 = {
            'id': 3,
            'name': 'category3'
        }
        category4 = {
            'id': 4,
            'name': 'category4'
        }

        list_category.append(category1)
        list_category.append(category2)
        list_category.append(category3)
        list_category.append(category4)

        resp = self.req_sess.get(self.fullpath+'/eshop/categories/list', params={'sort': 'name'})

        self.assertListEqual(resp.json(), list_category)

    def test_list_get_sort_by_cnt(self):
        list_category = []

        category1 = {
            'id': 1,
            'name': 'category1'
        }
        category2 = {
            'id': 2,
            'name': 'category2'
        }
        category3 = {
            'id': 3,
            'name': 'category3'
        }
        category4 = {
            'id': 4,
            'name': 'category4'
        }

        list_category.append(category3)
        list_category.append(category2)
        list_category.append(category1)
        list_category.append(category4)

        resp = self.req_sess.get(self.fullpath+'/eshop/categories/list', params={'sort': 'cnt'})

        self.assertListEqual(resp.json(), list_category)
