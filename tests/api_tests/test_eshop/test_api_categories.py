import unittest
from sqlalchemy.orm import scoped_session, sessionmaker
import zerorpc
from models import Base, SessionToken
from tests.constants import ZERORPC_SERVICE_URI
from tests.create_test_user import create
from tests.fixtures import create_categories, create_items, create_items_categories, create_categories_extras, \
    create_extras, create_cdn
from utils.connection import db_connect, create_session


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


def tearDownModule():
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")


class CategoriesTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.cl = zerorpc.Client(timeout=3000, heartbeat=100000)
        self.cl.connect(ZERORPC_SERVICE_URI)
        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)

    def tearDown(self):
        self.cl.close()
        self.session.close()

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
        IPC_pack = {
            'api_method': '/eshop/categories/{id}/info'.format(id=1),
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {}
        }
        resp = self.cl.route(IPC_pack)
        self.assertDictEqual(resp, data)

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

        IPC_pack = {
            'api_method': '/eshop/categories/{id}/extras'.format(id=1),
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {}
        }

        resp = self.cl.route(IPC_pack)

        self.assertListEqual(resp, list_extras)

    def test_items_get(self):
        IPC_pack = {
            'api_method': '/eshop/categories/{id}/items'.format(id=1),
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {}

        }

        resp = self.cl.route(IPC_pack)


    def test_list_get_has_items_true(self):
        IPC_pack = {
            'api_method': '/eshop/categories/list',
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {'has_items': 1}

        }
        resp = self.cl.route(IPC_pack)
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
        self.assertListEqual(resp, list_category)

    def test_list_get_has_items_false(self):
        IPC_pack = {
            'api_method': '/eshop/categories/list',
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {'has_items': 0}

        }

        category = {
            'id': 3,
            'name': 'category3'
        }

        list_category = []

        list_category.append(category)
        resp = self.cl.route(IPC_pack)
        self.assertListEqual(resp, list_category)

    def test_list_get_instock_true(self):
        IPC_pack = {
            'api_method': '/eshop/categories/list',
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {'instock': 1}

        }

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

        resp = self.cl.route(IPC_pack)

        self.assertListEqual(resp, list_category)

    def test_list_get_instock_false(self):
        IPC_pack = {
            'api_method': '/eshop/categories/list',
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {'instock': 0}

        }
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

        resp = self.cl.route(IPC_pack)

        self.assertListEqual(resp, list_category)

    def test_list_get_sort_by_name(self):
        IPC_pack = {
            'api_method': '/eshop/categories/list',
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {'sort': 'name'}

        }
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

        resp = self.cl.route(IPC_pack)

        self.assertListEqual(resp, list_category)

    def test_list_get_sort_by_cnt(self):
        IPC_pack = {
            'api_method': '/eshop/categories/list',
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {'sort': 'cnt'}

        }
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

        resp = self.cl.route(IPC_pack)

        self.assertListEqual(resp, list_category)



