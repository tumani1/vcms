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
    #engine.execute("drop schema public cascade; create schema public;")


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
        IPC_pack = {
            'api_method': 'eshop/categories/%s/info' % (id),
            'api_type': 'get',
            'x_token': self.session_token[1],
            'query_params': {}
        }
        resp = self.cl.route(IPC_pack)
        print resp