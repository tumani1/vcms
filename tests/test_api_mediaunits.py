import unittest

import zerorpc
from sqlalchemy.orm import sessionmaker, scoped_session

from create_test_user import create
from models import Base
from db_engine import db_connect
from unittest import skip


class MediaUnitsTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = db_connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        Base.metadata.create_all(self.engine)
        self.cl = zerorpc.Client()
        self.cl.connect("tcp://127.0.0.1:4242")
        create()
    @skip
    def test_info(self):
        IPC_pack = {'api_group':'mediaunits',
                    'api_method':'info',
                    'http_method':'get',
                    'api_format':'json',
                    'token':'echo_token',
                    'query_params':{
                        'id': 1}}
        resp = self.cl.route(IPC_pack)
        # resp = mashed_routes[('mediaunits','info','get')](**{'id': 1, 'user': db(lambda session: session.query(Users).first())()})
        self.assertTrue(resp)

    def tearDown(self):
        self.session.rollback()
        self.session.close()
        self.cl.close()