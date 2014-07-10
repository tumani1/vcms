import zerorpc
import unittest
from models import Base, SessionToken
from sqlalchemy.orm import sessionmaker, scoped_session
from utils.connection import db_connect, create_session
from fixtures import create, create_msgr_threads, create_users_msgr_threads, create_msgr_log


def setUpModule():
    engine = db_connect()
    #engine.execute("drop schema public cascade; create schema public;")
    session = create_session(bind=engine)
    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)
    create_msgr_threads(session)
    create_users_msgr_threads(session)
    create_msgr_log(session)






def tearDownModule():
    engine = db_connect()
    #engine.execute("drop schema public cascade; create schema public;")


class MsgrTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.cl = zerorpc.Client(timeout=3000, heartbeat=100000)
        self.cl.connect("tcp://127.0.0.1:4242", )
        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)

    def tearDown(self):
        self.cl.close()
        self.session.close()


    def test_info_get(self):
        IPC_pack = {'api_group': 'msgr',
                    'api_method': 'info',
                    'http_method': 'get',
                    'api_format': 'json',
                    'x_token': self.session_token[1],
                    'query_params': {'id': 1}
        }
        resp = self.cl.route(IPC_pack)
