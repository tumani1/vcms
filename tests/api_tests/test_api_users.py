# coding: utf-8

import zerorpc
import unittest


from models import Base, Users, UsersRels, UsersExtras, Extras, Cities,SessionToken
from models.users.constants import APP_USERSRELS_TYPE_FRIEND, APP_USERSRELS_TYPE_UNDEF

from utils.connection import get_session, db_connect, create_session
from utils.common import convert_to_utc

from tests.constants import ZERORPC_SERVICE_URI
from tests.fixtures import create, create_users_rels, create_scheme, create_topic, \
    create_users_values


def setUpModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")
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
    # engine.execute("drop schema public cascade; create schema public;")


class UsersTestCase(unittest.TestCase):

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

    def test_users_values_get(self):
        self.ipc_pack['api_method'] = 'values'
        self.ipc_pack['http_method'] = 'get'
        self.ipc_pack['query_params'] = {
            'topic': 'test1',
            'text': 'test',
            'user_id': 1
        }
        resp = self.zero_client.route(self.ipc_pack)
        self.assertDictEqual(resp[0], {'id': 1, 'value': 777})

    def test_test_users_list_get(self):
        self.ipc_pack['api_method'] = 'list'
        self.ipc_pack['http_method'] = 'get'
        self.ipc_pack['query_params'] = {
            'country': 'Test',
        }
        resp_dicts = self.zero_client.route(self.ipc_pack)
        users = self.session.query(Users).join(Cities).filter(Cities.name == 'Test')
        self.assertEqual(len(resp_dicts), users.count())
        users_dict = []
        for user in users:
            users_dict.append({
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'is_online': False,
                'gender': user.gender.code,
                'regdate': convert_to_utc(user.created),
                'lastvisit': convert_to_utc(user.last_visit) if user.last_visit else '',
                'city': user.city.name,
                'country': user.city.country.name,
            })

        for resp_dict in resp_dicts:
            user_d = filter(lambda i: i['id'] == resp_dict['id'], users_dict)[0]
            self.assertDictEqual(resp_dict, user_d)

    def test_users_info_get(self):
        self.ipc_pack['api_method'] = 'info'
        self.ipc_pack['http_method'] = 'get'

        self.ipc_pack['query_params'] = {
            'id': 1
        }
        resp_dict = self.zero_client.route(self.ipc_pack)
        user = self.session.query(Users).get(1)
        user_dict = {
            'id': user.id,
            'firstname': str(user.firstname),
            'lastname': str(user.lastname),
            'is_online': False,
            'gender': str(user.gender.code),
            'regdate': convert_to_utc(user.created),
            'lastvisit': convert_to_utc(user.last_visit) if user.last_visit else '',
            'city': str(user.city.name),
            'country': str(user.city.country.name),
        }
        self.assertDictEqual(resp_dict, user_dict)

    def test_users_friendship_get(self):
        self.ipc_pack['api_method'] = 'friendship'
        self.ipc_pack['http_method'] = 'get'
        self.ipc_pack['x_token'] = SessionToken.generate_token(1, session=self.session)[1]
        self.ipc_pack['query_params'] = {
            'id': 2
        }
        resp = self.zero_client.route(self.ipc_pack)
        self.assertEqual(resp, APP_USERSRELS_TYPE_FRIEND)
        self.ipc_pack['query_params'] = {
            'id': 3
        }
        resp = self.zero_client.route(self.ipc_pack)
        self.assertEqual(resp, APP_USERSRELS_TYPE_UNDEF)

    def test_users_friends_get(self):
        self.ipc_pack['api_method'] = 'friends'
        self.ipc_pack['http_method'] = 'get'
        self.ipc_pack['query_params'] = {
            'id': 1
        }
        resp_dicts = self.zero_client.route(self.ipc_pack)
        subquery = self.session.query(UsersRels.partner_id).filter_by(user_id=1, urStatus=APP_USERSRELS_TYPE_FRIEND).subquery()
        friends = self.session.query(Users).filter(Users.id.in_(subquery)).all()
        users_dict = []
        for user in friends:
            users_dict.append({
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'is_online': False,
            })
        for resp_dict in resp_dicts:
            user_dict = filter(lambda i: i['id'] == resp_dict['id'], users_dict)[0]
            self.assertDictEqual(resp_dict, user_dict)

    def test_users_extras_get(self):
        self.ipc_pack['api_method'] = 'extras'
        self.ipc_pack['http_method'] = 'get'
        self.ipc_pack['query_params'] = {
            'user_id': 1,
        }

        resp_dicts = self.zero_client.route(self.ipc_pack)
        extras = self.session.query(Extras).join(UsersExtras).filter(UsersExtras.user_id == 1).all()
        extras_dict = []
        for extra in extras:
            extras_dict.append({
                'id': extra.id,
                'type': extra.type.code,
                'title': extra.title,
                'title_orig': extra.title_orig,
                'description': extra.description,
                'location': extra.location,
                'created': convert_to_utc(extra.created),
            })

        for resp_dict in resp_dicts:
            extra_dict = filter(lambda i: i['id'] == resp_dict['id'], extras_dict)[0]
            self.assertDictEqual(resp_dict, extra_dict)
