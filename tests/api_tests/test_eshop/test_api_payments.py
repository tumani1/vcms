import unittest
from sqlalchemy.orm import scoped_session, sessionmaker
import zerorpc
from models import Base, SessionToken
from tests.constants import ZERORPC_SERVICE_URI
from tests.create_test_user import create
from tests.fixtures import create_cart, create_payments
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
    create_payments(session)


def tearDownModule():
    engine = db_connect()
    #engine.execute("drop schema public cascade; create schema public;")


class PaymentsListTestCase(unittest.TestCase):
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

    def test_payments_list_get(self):
        IPC_pack = {
            'api_method': '/eshop/payments/list',
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {}
        }

        resp = self.cl.route(IPC_pack)

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

        self.assertDictEqual(resp, data)

