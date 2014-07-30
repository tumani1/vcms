# coding: utf-8

import zerorpc
import unittest

from tests.constants import ZERORPC_SERVICE_URI
from tests.fixtures import create, create_users_rels, create_scheme, create_topic, \
    create_users_values, create_persons

from models import Base, Users, UsersRels, UsersExtras, \
    Extras, Cities, SessionToken

from models.users.constants import APP_USERSRELS_TYPE_FRIEND, APP_USERSRELS_TYPE_UNDEF

from utils.common import convert_to_utc
from utils.connection import get_session, db_connect, create_session



def setUpModule():
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")
    session = create_session(bind=engine)
    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)
    create_users_rels(session)
    create_topic(session)
    create_scheme(session)
    create_users_values(session)
    session.close()


def tearDownModule():
    engine = db_connect()
    engine.execute("drop schema public cascade; create schema public;")


class PersonInfoTestCase(unittest.TestCase):

    def setUp(self):
        self.session = get_session()
        self.zero_client = zerorpc.Client(timeout=3000, heartbeat=100000)
        self.zero_client.connect(ZERORPC_SERVICE_URI)
        self.ipc_pack = {
            'api_group': 'users',
            'api_method': '',
            'http_method': 'get',
            'api_format': 'json',
            'x_token': None,
            'query_params': {}
        }


    def tearDown(self):
        self.session.close()
        self.zero_client.close()


    def test_get_person_info(self):
        self.ipc_pack['api_method'] = 'info'
        self.ipc_pack['http_method'] = 'get'

        self.ipc_pack['query_params'] = {
            'id': 1
        }

        resp_dict = self.zero_client.route(self.ipc_pack)
        user = self.session.query(Users).get(1)
        user_dict = {
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'is_online': False,
            'gender': user.gender.code,
            'regdate': convert_to_utc(user.created),
            'lastvisit': convert_to_utc(user.last_visit) if user.last_visit else '',
            'city': user.city.name,
            'country': user.city.country.name,
        }

        self.assertDictEqual(resp_dict, user_dict)
