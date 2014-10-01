import unittest
from sqlalchemy.orm import scoped_session, sessionmaker
import zerorpc
from models import Base, SessionToken
from tests.constants import ZERORPC_SERVICE_URI
from tests.create_test_user import create
from tests.fixtures import create_categories, create_items, create_items_categories, create_categories_extras, \
    create_extras, create_cdn, create_items_extras, create_variants, create_variants_extras
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
    create_items_extras(session)
    create_variants(session)
    create_variants_extras(session)


def tearDownModule():
    engine = db_connect()
    #engine.execute("drop schema public cascade; create schema public;")


class ItemsInfoTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))
        cls.cl = zerorpc.Client(timeout=3000, heartbeat=100000)
        cls.cl.connect(ZERORPC_SERVICE_URI)
        cls.user_id = 1
        cls.session_token = SessionToken.generate_token(cls.user_id, session=cls.session)

    @classmethod
    def tearDown(cls):
        cls.cl.close()
        cls.session.close()

    def test_items_info_get(self):
        list_extras = []
        IPC_pack = {
            'api_method': '/eshop/items/{id}/info'.format(id=1),
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {}
        }

        resp = self.cl.route(IPC_pack)
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

        self.assertDictEqual(resp, data)


class ItemsVariantsTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))
        cls.cl = zerorpc.Client(timeout=3000, heartbeat=100000)
        cls.cl.connect(ZERORPC_SERVICE_URI)
        cls.user_id = 1
        cls.session_token = SessionToken.generate_token(cls.user_id, session=cls.session)

    @classmethod
    def tearDown(cls):
        cls.cl.close()
        cls.session.close()

    def test_items_variants_get(self):
        IPC_pack = {
            'api_method': '/eshop/items/{id}/variants'.format(id=1),
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {}
        }

        resp = self.cl.route(IPC_pack)
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
            'available_cnt': 1.0
        }

        data_list.append(data)

        self.assertListEqual(resp, data_list)


class ItemsBookTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))
        cls.cl = zerorpc.Client(timeout=3000, heartbeat=100000)
        cls.cl.connect(ZERORPC_SERVICE_URI)
        cls.user_id = 1
        cls.session_token = SessionToken.generate_token(cls.user_id, session=cls.session)

    @classmethod
    def tearDown(cls):
        cls.cl.close()
        cls.session.close()

    def test_items_book_post(self):
        IPC_pack = {
            'api_method': '/eshop/items/{id}/book'.format(id=1),
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {}
        }


class ItemsListTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))
        cls.cl = zerorpc.Client(timeout=3000, heartbeat=100000)
        cls.cl.connect(ZERORPC_SERVICE_URI)
        cls.user_id = 1
        cls.session_token = SessionToken.generate_token(cls.user_id, session=cls.session)

    @classmethod
    def tearDown(cls):
        cls.cl.close()
        cls.session.close()

    def test_items_list_get(self):
        IPC_pack = {
            'api_method': '/eshop/items/list',
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {}
        }

        resp = self.cl.route(IPC_pack)

        list_extras1 = []
        list_extras2 = []
        extras1 = {
            'id': 1,
            'description': 'test test',
            'created': 1388534400.0,
            'location': 'russia',
            'title': 'test',
            'type': 'Video',
            'title_orig': 'test'
        }
        extras2 = {
            'id': 2,
            'description': 'test1 test',
            'created': 1388534400.0,
            'location': 'russia',
            'title': 'test1',
            'type': 'Video',
            'title_orig': 'test1'
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

        list_extras2.append(extras2)

        mShopItem2  = {
            'name': 'item2',
            'description': 'item2_test',
            'instock': True,
            'id': 2,
            'is_digital': True,
            'price': None,
            'price_old': None,
            'extras': list_extras2,
            'relation': {}
        }

        mShopItem3  = {
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

        mShopItem4  = {
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

        list_mShopItem = []

        list_mShopItem.append(mShopItem1)
        list_mShopItem.append(mShopItem2)
        list_mShopItem.append(mShopItem4)
        list_mShopItem.append(mShopItem3)

        data = {
            'cnt': 4,
            'total_cnt': 4,
            'items': list_mShopItem
        }

        self.assertDictEqual(resp, data)

