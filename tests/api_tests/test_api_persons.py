# coding: utf-8

import zerorpc
import unittest

from tests.constants import ZERORPC_SERVICE_URI
from tests.fixtures import create, create_scheme, create_topic, create_cdn, \
    create_users_values, create_persons, create_person_extras, create_extras, \
    create_persons_values, create_media, create_media_units

from models import Base, Users,\
    Extras, Cities, SessionToken, Persons, UsersPersons

from utils.common import detetime_to_unixtime
from utils.connection import get_session, db_connect, create_session


def setUpModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")
    session = create_session(bind=engine)
    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)
    create_topic(session)
    create_scheme(session)
    create_users_values(session)
    create_cdn(session)
    create_extras(session)
    create_persons(session)
    create_person_extras(session)
    create_persons_values(session)
    create_media_units(session)
    create_media(session)
    session.close()


def tearDownModule():
    engine = db_connect()
    # engine.execute("drop schema public cascade; create schema public;")


##################################################################################
class PersonInfoTestCase(unittest.TestCase):

    def setUp(self):
        self.session = get_session()

        self.zero_client = zerorpc.Client(timeout=3000, heartbeat=100000)
        self.zero_client.connect(ZERORPC_SERVICE_URI)

        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)


    def tearDown(self):
        self.session.close()
        self.zero_client.close()


    def test_get_person_info(self):
        person_id = 1
        ipc_pack = {
            'api_group': 'persons',
            'api_method': 'info',
            'http_method': 'get',
            'api_format': 'json',
            'x_token': self.session_token[1],
            'query_params': {
                'id': person_id,
            }
        }

        resp = self.zero_client.route(ipc_pack)

        persons = self.session.query(Persons).filter(Persons.id == person_id).all()
        self.assertEqual(1, len(persons))
        persons = persons[0]

        up = self.session.query(UsersPersons).filter(UsersPersons.user_id == self.user_id, UsersPersons.person_id == person_id).all()
        self.assertEqual(0, len(up))

        if len(up):
            up = up[0]
            relation = {
                'liked': up.check_liked,
                'subscribed': up.check_subscribed,
            }
        else:
            relation = {}

        user = self.session.query(Users).filter(Users.id == persons.user_id).first()

        temp = {
            'id': persons.id,
            'firstname': persons.firstname,
            'lastname': persons.lastname,
            'relation': relation,
            'user': {
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'is_online': True,
                'gender': user.gender.code,
                'regdate': detetime_to_unixtime(user.created),
                'lastvisit': detetime_to_unixtime(user.last_visit) if user.last_visit else '',
                'city': user.city.name,
                'country': user.city.country.name,
            }
        }

        self.assertDictEqual(temp, resp)


##################################################################################
class PersonListTestCase(unittest.TestCase):

    def setUp(self):
        self.session = get_session()

        self.zero_client = zerorpc.Client(timeout=3000, heartbeat=100000)
        self.zero_client.connect(ZERORPC_SERVICE_URI)

        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)


    def tearDown(self):
        self.session.close()
        self.zero_client.close()


    def test_get_person_list(self):
        ipc_pack = {
            'api_group': 'persons',
            'api_method': 'list',
            'http_method': 'get',
            'api_format': 'json',
            'x_token': self.session_token[1],
            'query_params': {}
        }

        resp = self.zero_client.route(ipc_pack)
        self.assertEqual(5, len(resp))


##################################################################################
class PersonLikeTestCase(unittest.TestCase):

    def setUp(self):
        self.session = get_session()

        self.zero_client = zerorpc.Client(timeout=3000, heartbeat=100000)
        self.zero_client.connect(ZERORPC_SERVICE_URI)

        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)


    def tearDown(self):
        self.session.close()
        self.zero_client.close()


    def test_echo_get(self):
        person = 2
        IPC_pack = {
            "api_group": "persons",
            "api_method": "like",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "get",
            "query_params": {
                "id": person,
            }
        }

        resp = self.zero_client.route(IPC_pack)
        temp = {'liked': 0}

        self.assertDictEqual(temp, resp)


    def test_echo_post(self):
        person = 2
        IPC_pack = {
            "api_group": "persons",
            "api_method": "like",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "post",
            "query_params": {
                 "id": person,
            }
        }

        resp = self.zero_client.route(IPC_pack)
        self.assertEqual(resp, None)

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        person = UsersPersons.get_user_person(user=user, person_id=person, session=self.session).all()
        self.assertEqual(1, len(person))
        person = person[0]

        self.assertNotEqual(person.liked, None)


    def test_fail_echo_post(self):
        person = 1
        IPC_pack = {
            "api_group": "persons",
            "api_method": "subscribe",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "post",
            "query_params": {
                "id": person,
            }
        }

        resp = self.zero_client.route(IPC_pack)
        self.assertTrue('error' in resp)


    def test_echo_delete(self):
        person = 2
        IPC_pack = {
            "api_group": "persons",
            "api_method": "like",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "delete",
            "query_params": {
                 "id": person,
            }
        }

        resp = self.zero_client.route(IPC_pack)
        self.assertEqual(resp, None)

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        person = UsersPersons.get_user_person(user=user, person_id=person, session=self.session).all()
        self.assertEqual(0, len(person))


##################################################################################
class PersonSubscribeTestCase(unittest.TestCase):

    def setUp(self):
        self.session = get_session()

        self.zero_client = zerorpc.Client(timeout=3000, heartbeat=100000)
        self.zero_client.connect(ZERORPC_SERVICE_URI)

        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)


    def tearDown(self):
        self.session.close()
        self.zero_client.close()


    def test_echo_get(self):
        person = 2
        IPC_pack = {
            "api_group": "persons",
            "api_method": "subscribe",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "get",
            "query_params": {
                "id": person,
            }
        }

        resp = self.zero_client.route(IPC_pack)
        temp = {'subscribed': 0}

        self.assertDictEqual(temp, resp)


    def test_fail_echo_post(self):
        person = 1
        IPC_pack = {
            "api_group": "persons",
            "api_method": "subscribe",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "post",
            "query_params": {
                "id": person,
            }
        }

        resp = self.zero_client.route(IPC_pack)
        self.assertTrue('error' in resp)


    def test_echo_post(self):
        person = 2
        IPC_pack = {
            "api_group": "persons",
            "api_method": "subscribe",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "post",
            "query_params": {
                "id": person,
            }
        }

        resp = self.zero_client.route(IPC_pack)
        self.assertEqual(resp, None)

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        person = UsersPersons.get_user_person(user=user, person_id=person, session=self.session).all()
        self.assertEqual(1, len(person))
        person = person[0]

        self.assertNotEqual(person.subscribed, None)


    def test_echo_delete(self):
        person = 2
        IPC_pack = {
            "api_group": "persons",
            "api_method": "subscribe",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "delete",
            "query_params": {
                "id": person,
            }
        }

        resp = self.zero_client.route(IPC_pack)
        self.assertEqual(resp, None)

        user = Users.get_users_by_id(session=self.session, users_id=[self.user_id]).first()

        person = UsersPersons.get_user_person(user=user, person_id=person, session=self.session).all()
        self.assertEqual(0, len(person))


##################################################################################
class PersonExtrasTestCase(unittest.TestCase):

    def setUp(self):
        self.session = get_session()

        self.zero_client = zerorpc.Client(timeout=3000, heartbeat=100000)
        self.zero_client.connect(ZERORPC_SERVICE_URI)

        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)


    def tearDown(self):
        self.session.close()
        self.zero_client.close()


    def test_echo(self):
        person = 2
        IPC_pack = {
            "api_group": "persons",
            "api_method": "extras",
            "api_format": "json",
            "x_token": self.session_token[1],
            "http_method": "get",
            "query_params": {
                "id": person,
            }
        }

        resp = self.zero_client.route(IPC_pack)
        temp = [
            {
                'description': 'test test',
                'created': 1388534400.0,
                'title': 'test',
                'title_orig': 'test',
                'location': 'russia',
                'type': 'v',
                'id': 1
            }, {
                'description': 'test2 test',
                'created': 1388534400.0,
                'title': 'test2',
                'title_orig': 'test2',
                'location': 'russia',
                'type': 'a',
                'id': 3
            }
        ]

        self.assertEqual(2, len(resp))
        self.assertListEqual(temp, resp)


##################################################################################
class PersonValuesTestCase(unittest.TestCase):

    def setUp(self):
        self.session = get_session()

        self.zero_client = zerorpc.Client(timeout=3000, heartbeat=100000)
        self.zero_client.connect(ZERORPC_SERVICE_URI)

        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)


    def tearDown(self):
        self.session.close()
        self.zero_client.close()


    def test_echo(self):
        person = 2
        IPC_pack = {
            "api_group": "persons",
            "api_method": "values",
            "api_format": "json",
            "http_method": "get",
            "query_params": {
                'id': person,
                'name': ['shm1', 'shm2'],
                'value': '777',
            }
        }

        resp = self.zero_client.route(IPC_pack)
        temp = [
            {
                'name': 3,
                'value': 777
            }, {
                'name': 4,
                'value': 777
            }
        ]
        self.assertEqual(temp, resp)


##################################################################################
class PersonMediaTestCase(unittest.TestCase):

    def setUp(self):
        self.session = get_session()

        self.zero_client = zerorpc.Client(timeout=3000, heartbeat=100000)
        self.zero_client.connect(ZERORPC_SERVICE_URI)

        self.user_id = 1
        self.session_token = SessionToken.generate_token(self.user_id, session=self.session)


    def tearDown(self):
        self.session.close()
        self.zero_client.close()


    def test_echo(self):
        person = 1
        IPC_pack = {
            "api_group": "persons",
            "api_method": "media",
            "api_format": "json",
            "http_method": "get",
            "query_params": {
                'id': person,
            }
        }

        resp = self.zero_client.route(IPC_pack)
        temp = [
            {
                'description': 'test_desc1',
                'title': 'media1',
                'locations': [],
                'releasedate': None,
                'title_orig': 'test_media1',
                'duration': None,
                'relation': {},
                'id': 1
            }
        ]

        self.assertEqual(temp, resp)
