import unittest
from sqlalchemy.orm import scoped_session, sessionmaker
import zerorpc
from models import Base, SessionToken
from tests.constants import ZERORPC_SERVICE_URI
from tests.create_test_user import create
from tests.fixtures import create_cart, create_items_carts, create_items, create_items_objects, create_variants_extras, \
    create_cdn, create_variants, create_extras, create_items_extras, create_payments, create_cart_log
from utils.connection import db_connect, create_session


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
    #engine.execute("drop schema public cascade; create schema public;")


class CartStatTestCase(unittest.TestCase):
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

    def test_cart_stat_get(self):
        IPC_pack = {
            'api_method': '/eshop/cart/stat',
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {}
        }

        resp = self.cl.route(IPC_pack)

        data = {
            'items_cnt': 1,
            'total_cnt': 1,
            'cost': 10,
            'id': 1
        }

        self.assertDictEqual(resp, data)


class CartItemsTestCase(unittest.TestCase):
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

    def test_cart_items_get(self):
        IPC_pack = {
            'api_method': '/eshop/cart/items',
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

        self.assertListEqual(resp, list_data)


class CartsTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.engine = db_connect()
        cls.session = scoped_session(sessionmaker(bind=cls.engine))
        cls.cl = zerorpc.Client(timeout=3000, heartbeat=100000)
        cls.cl.connect(ZERORPC_SERVICE_URI)
        cls.user_id = 1
        cls.session_token = SessionToken.generate_token(cls.user_id, session=cls.session)
        cls.IPC_pack = {
            'api_method': '',
            'api_type': 'get',
            'x_token': cls.session_token[1],
            'query_params': {}
        }

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
        cls.cl.close()
        cls.session.close()

    def test_carts_list_get(self):
        self.IPC_pack['api_method'] = '/eshop/carts/list'
        resp = self.cl.route(self.IPC_pack)

        data = {
            'cnt': 1,
            'total_cnt': 1,
            'items': self.list_mShopCart
        }

        self.assertDictEqual(resp, data)

    def test_carts_info_get_by_id(self):
        self.IPC_pack['api_method'] = '/eshop/carts/{id}/info'.format(id=1)
        resp = self.cl.route(self.IPC_pack)

        self.assertDictEqual(resp, self.mShopCart)

    def test_carts_items_get_by_id(self):
        self.IPC_pack['api_method'] = '/eshop/carts/{id}/items'.format(id=1)
        resp = self.cl.route(self.IPC_pack)

        data = []
        data.append(self.mShopCartItem)

        self.assertListEqual(resp, data)

    def test_carts_log_get_by_id(self):
        self.IPC_pack['api_method'] = '/eshop/carts/{id}/log'.format(id=1)

        resp = self.cl.route(self.IPC_pack)

        data = []

        data.append(self.mShopCartLog)

        self.assertListEqual(resp, data)


