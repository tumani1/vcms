# coding: utf-8

import re

from api import authorize
from utils.connection import create_session, db_connect, mongo_connect
from zerorpcservices.additional import raven_report
from utils.exceptions import APIException


class BaseService(object):

    def __init__(self, routes):
        self.connect = db_connect()
        self.mongodb_session = mongo_connect()
        self.routes = routes


    def get_url(self, IPC_pack):
        path_parse = IPC_pack['api_method'].split('/', 2)
        group = self.routes[path_parse[1]]

        for item in group:
            method = IPC_pack['api_type'].lower()
            match = re.match(item[0], u'/'.join(path_parse[2:]))

            if match and method in item[1]:
                return match.groupdict(), item[1][method]

        raise


    @raven_report
    def route(self, IPC_pack):
        session = create_session(bind=self.connect, expire_on_commit=False)

        try:
            auth_user = authorize(IPC_pack, session=session)

            params = {
                'session': session,
                'auth_user': auth_user,
                'query': IPC_pack['query_params']
            }

            url_params, api_method = self.get_url(IPC_pack)
            params.update(url_params)

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


    @raven_report
    def content_route(self, IPC_pack):
        session = create_session(bind=self.connect, expire_on_commit=False)

        try:
            path_parse = IPC_pack['api_method'].split('/', 4)
            mashed_key = (path_parse[1], path_parse[2], IPC_pack['api_type'].lower())

            api_method = self.mashed_routes[mashed_key]
            response = {
                'code': 200,
                'location': api_method(pk=path_parse[3], session=session)
            }
        except Exception as e:
            session.rollback()
            response = {'code': 404, 'message': e.message}
        finally:
            session.close()

        return response
