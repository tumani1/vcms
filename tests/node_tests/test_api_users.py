# coding: utf-8
import requests
import unittest

from tests.fixtures import create, create_users_rels, create_scheme, create_topic, \
    create_users_values
from models import Base
from models.users import Users, UsersRels, UsersExtras
from models.users.constants import APP_USERSRELS_BLOCK_TYPE_RECIEVE, APP_USERSRELS_BLOCK_TYPE_SEND
from models.extras import Extras
from models.users.constants import APP_USERSRELS_TYPE_FRIEND, APP_USERSRELS_TYPE_UNDEF
from models.contents import Cities
from settings import NODE
from utils.connection import db_connect, create_session
from utils.common import detetime_to_unixtime


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
    # engine.execute("drop schema public cascade; create schema public;")


class UsersTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect().connect()
        self.session = create_session(bind=self.engine, expire_on_commit=False)

        self.h, self.p = NODE['rest_ws_serv']['host'], NODE['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)

        self.req_sess = requests.Session()

        self.user_id = 1

        resp = self.req_sess.post(self.fullpath+'/auth/login', data={'email': 'test1@test.ru', 'password': 'Test1'})
        self.token = resp.json()['token']

    def tearDown(self):
        self.session.close()
        self.req_sess.close()
        self.engine.close()

    def test_users_values_get(self):
        id = 1
        resp = self.req_sess.get(self.fullpath + '/users/%s/values' % (id), params={'topic': 'test1', 'text': 'test'})
        self.assertDictEqual(resp.json()[0], {u'name': 1, u'value': 777})

    def test_users_list_get(self):
        resp = self.req_sess.get(self.fullpath + '/users/list', params={'country': 'Test'})
        users = self.session.query(Users).join(Cities).filter(Cities.name == 'Test')
        resp_dicts = resp.json()[0]
        self.assertEqual(len(resp_dicts), users.count())
        users_dict = []
        for user in users:
            users_dict.append({
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'is_online': False,
                'gender': user.gender.code,
                'regdate': detetime_to_unixtime(user.created),
                'lastvisit': detetime_to_unixtime(user.last_visit) if user.last_visit else '',
                'city': user.city.name,
                'country': user.city.country.name,
            })

        for resp_dict in resp_dicts:
            user_d = filter(lambda i: i['id'] == resp_dict['id'], users_dict)[0]
            self.assertDictEqual(resp_dict, user_d)

    def test_users_info_get(self):
        id = 1
        resp = self.req_sess.get(self.fullpath + '/users/%s/info' % (id), params={})
        resp_dict = resp.json()
        user = self.session.query(Users).get(1)
        user_dict = {
            u'id': user.id,
            u'firstname': user.firstname,
            u'lastname': user.lastname,
            u'is_online': False,
            u'gender': user.gender.code,
            u'regdate': detetime_to_unixtime(user.created),
            u'lastvisit': detetime_to_unixtime(user.last_visit) if user.last_visit else '',
            u'city': user.city.name,
            u'country': user.city.country.name,
        }
        self.assertDictEqual(resp_dict, user_dict)

    def test_users_friendship_get(self):
        id = 2
        resp = self.req_sess.get(self.fullpath + '/users/%s/friendship' % (id), headers={'token': self.token}, params={})
        self.assertEqual(resp.json(), APP_USERSRELS_TYPE_FRIEND)
        id = 3
        resp = self.req_sess.get(self.fullpath + '/users/%s/friendship' % (id), headers={'token': self.token}, params={})
        self.assertEqual(resp.json(), APP_USERSRELS_TYPE_UNDEF)

    def test_users_friends_get(self):
        id = 1
        resp = self.req_sess.get(self.fullpath + '/users/%s/friends' % (id), params={})
        resp_dicts = resp.json()[0]
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
        id = 1
        resp = self.req_sess.get(self.fullpath + '/users/%s/extras' % (id), params={})
        resp_dicts = resp.json()[0]
        extras = self.session.query(Extras).join(UsersExtras).filter(UsersExtras.user_id == id).all()
        extras_dict = []
        for extra in extras:
            extras_dict.append({
                'id': extra.id,
                'type': extra.type.code,
                'title': extra.title,
                'title_orig': extra.title_orig,
                'description': extra.description,
                'location': extra.location,
                'created': detetime_to_unixtime(extra.created),
            })

        for resp_dict in resp_dicts:
            extra_dict = filter(lambda i: i['id'] == resp_dict['id'], extras_dict)[0]
            self.assertDictEqual(resp_dict, extra_dict)

    def test_users_blacklist_post(self):
        data = {}
        id = 2
        resp = self.req_sess.post(self.fullpath + '/users/%s/blacklist' % (id), headers={'token': self.token}, params=data)
        user_rels =self.session.query(UsersRels).filter_by(user_id=self.user_id, partner_id=id).first()
        partner_rels = self.session.query(UsersRels).filter_by(user_id=id, partner_id=self.user_id).first()
        self.assertEqual(user_rels.blocked, APP_USERSRELS_BLOCK_TYPE_SEND)
        self.assertEqual(partner_rels.blocked, APP_USERSRELS_BLOCK_TYPE_RECIEVE)

    def test_users_blacklist_delete(self):
        data = {}
        id = 3
        resp = self.req_sess.delete(self.fullpath + '/users/%s/blacklist' % (id), headers={'token': self.token}, params=data)
        user_rels =self.session.query(UsersRels).filter_by(user_id=self.user_id, partner_id=id).first()
        partner_rels = self.session.query(UsersRels).filter_by(user_id=id, partner_id=self.user_id).first()
        self.assertEqual(user_rels.blocked, APP_USERSRELS_BLOCK_TYPE_RECIEVE)
        self.assertEqual(partner_rels.blocked, APP_USERSRELS_BLOCK_TYPE_SEND)