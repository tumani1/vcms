import zerorpc
import unittest
from models import Base, SessionToken, Users
from sqlalchemy.orm import sessionmaker, scoped_session
from db_engine.dbe import db_connect
from fixtures import create_media_units, create_topic, create


def setUpModule():
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")

    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create()


def tearDownModule():
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")


class UsersTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.cl = zerorpc.Client(timeout=3000)
        self.cl.connect("tcp://127.0.0.1:4242", )
        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)

    def tearDown(self):
        self.cl.close()
        self.session.close()

    def test_info_get(self):
        IPC_pack = {'api_group': 'user',
                    'api_method': 'info',
                    'http_method': 'get',
                    'api_format': 'json',
                    'x_token': self.session_token[1],
                    'query_params': {}
        }
        temp = {
                'city': 'Test',
                'userpic': 'Test',
                'firstname': 'Test',
                'country': 'Test',
                'time_zone': 'UTC',
                'lastname': 'Test',
                'id': 1
        }
        resp = self.cl.route(IPC_pack)
        self.assertDictEqual(resp, temp)

    def test_info_put(self):
        IPC_pack = {'api_group': 'user',
                    'api_method': 'info',
                    'http_method': 'put',
                    'api_format': 'json',
                    'x_token': self.session_token[1],
                    'query_params': {'firstname': 'Ivan', 'lastname': 'Ivanov'}
        }
        resp = self.cl.route(IPC_pack)
        test_user = self.session.query(Users).filter_by(id=self.user_id).first()
        self.assertEqual(test_user.firstname, IPC_pack['query_params']['firstname'])
        self.assertEqual(test_user.lastname, IPC_pack['query_params']['lastname'])

    def test_values_put(self):
        IPC_pack = {'api_group': 'user',
                    'api_method': 'values',
                    'http_method': 'put',
                    'api_format': 'json',
                    'x_token': self.session_token[1],
                    'query_params': {}
        }
        resp = self.cl.route(IPC_pack)