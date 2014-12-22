# coding: utf-8

import memcache

from api import authorize
from sqlalchemy.orm import sessionmaker, scoped_session
from zerorpcservices.additional import raven_report

from utils.common import get_api_by_url
from utils.exceptions import APIException
from utils.connection import db_connect, mongo_connect


class BaseService(object):

    def __init__(self, routes):
        self.routes = routes
        self.default_params = {}

        self.connect = db_connect()
        self.__session = scoped_session(sessionmaker(self.connect, expire_on_commit=False))

        self.mongodb_session = mongo_connect()

        self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    @raven_report
    def route(self, IPC_pack):
        session = self.__session()
        try:
            auth_user = authorize(IPC_pack, session=session)

            params, api_method = get_api_by_url(self.routes, IPC_pack)
            params.update({
                'session': session,
                'auth_user': auth_user,
                'query_params': IPC_pack['query_params'],
                'meta': IPC_pack.get('meta', {}),
                'mc': self.mc
            })
            api_params = self.default_params.copy()
            api_params.update(params)
            response = api_method(**api_params)

        except APIException as e:
            session.rollback()
            response = {'exception': {'code': e.code,
                                      'message': e.message}}
        except Exception as e:
            session.rollback()
            response = {'exception': {'code': 400,
                                      'message': 'Bad Request'}}
        finally:
            session.close()

        return response or ([] if isinstance(response, list) else {})
