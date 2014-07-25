# coding: utf-8
import yaml
import requests
import unittest
import json
from models import Base
from os.path import join
from utils.connection import db_connect, create_session
from fixtures import create, create_msgr_threads, create_users_msgr_threads, create_msgr_log
from settings import CONFIG_PATH
from websocket import create_connection
from utils.connection import get_session


def setUpModule():
    engine = db_connect()
    session = create_session(bind=engine)
    # Create table
    Base.metadata.create_all(bind=engine)

    # Fixture
    create(session)
    create_msgr_threads(session)
    create_users_msgr_threads(session)
    create_msgr_log(session)



class MsgrTestCase(unittest.TestCase):

    def setUp(self):
        with open(join(CONFIG_PATH, 'node_service.yaml')) as file:
            conf = yaml.safe_load(file)
        self.h, self.p = conf['rest_ws_serv']['host'], conf['rest_ws_serv']['port']
        self.fullpath = 'http://{}:{}'.format(self.h, self.p)
        self.req_sess = requests.Session()
        self.ws = create_connection('ws://{}:{}'.format(self.h, self.p))
        db_sess = get_session()
        create(db_sess)
        self.user_id = 1

    def tearDown(self):
        self.ws.close()

    def test_info_get(self):
        data = {
            'firstname': 'test',
            'lastname': 'test',
            'email': 'test@mail.ru',
            'pswd1': '123',
            'pswd2': '123',
            'city_id': 1
        }
        self.req_sess.post(self.fullpath + '/auth/register', data=data)
        login = self.req_sess.post(self.fullpath+'/auth/login', data={
            'email': 'tumany1@yandex.ru',
            'password': '123'
        })
        token = json.loads(login.text)['token']
        resp = self.req_sess.get(self.fullpath+'/msgr/1/info', headers={'token': token})
        print resp

    # def test_stat_get(self):
    #     IPC_pack = {
    #         'api_group': 'msgr',
    #         'api_method': 'stat',
    #         'http_method': 'get',
    #         'api_format': 'json',
    #         'x_token': self.session_token[1],
    #         'query_params': {}
    #     }
    #     resp = self.cl.route(IPC_pack)
    #     param = {'new_msgs': 1}
    #     self.assertDictEqual(resp, param)
    #
    # def test_create_put(self):
    #     IPC_pack = {
    #         'api_group': 'msgr',
    #         'api_method': 'create',
    #         'http_method': 'put',
    #         'api_format': 'json',
    #         'x_token': self.session_token[1],
    #         'query_params': {'user_ids': [1, 2], 'text': 'test'}
    #     }
    #     resp = self.cl.route(IPC_pack)
    #
    # def test_list_get(self):
    #     IPC_pack = {
    #         'api_group': 'msgr',
    #         'api_method': 'list',
    #         'http_method': 'get',
    #         'api_format': 'json',
    #         'x_token': self.session_token[1],
    #         'query_params': {'user_author': [1, 2]}
    #     }
    #     resp = self.cl.route(IPC_pack)