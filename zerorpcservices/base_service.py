# coding: utf-8

import re

from api import authorize
from utils.connection import create_session, db_connect, mongo_connect
from zerorpcservices.additional import raven_report
from utils.exceptions import APIException, NoSuchMethodException


class BaseService(object):

    def __init__(self, routes):
         self.routes = routes
         self.connect = db_connect()
         self.mongodb_session = mongo_connect()


    def get_url(self, IPC_pack):
        path_parse = IPC_pack['api_method'].split('/', 2)
        group = self.routes[path_parse[1]]

        for item in group:
            method = IPC_pack['api_type'].lower()
            match = re.match(item[0], u'/'.join(path_parse[2:]))

            if match and method in item[1]:
                return match.groupdict(), item[1][method]

        raise NoSuchMethodException


    @raven_report
    def route(self, IPC_pack):
        session = create_session(bind=self.connect, expire_on_commit=False)

        try:
            auth_user = authorize(IPC_pack, session=session)

            params, api_method = self.get_url(IPC_pack)
            params.update({
                'session': session,
                'auth_user': auth_user,
                'query': IPC_pack['query_params']
            })

            response = api_method(**params)

        except APIException as e:
            session.rollback()
            response = {'error': {'code': e.code,
                                  'message': e.message}}
        except Exception as e:
            session.rollback()
            response = {'error': {'code': 404,
                                  'message': 'Bad Request'}}
        finally:
            session.close()

        return response
