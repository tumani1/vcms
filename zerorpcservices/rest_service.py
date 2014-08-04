# coding: utf-8
import argparse
import zerorpc
import settings as conf
from api import routes
from api import authorize
from utils.connection import create_session, db_connect, mongo_connect
from zerorpcservices.additional import raven_report
from utils.exceptions import APIException


class ZeroRpcRestApiService(object):

    def __init__(self):
        self.connect = db_connect()
        self.mongodb_session = mongo_connect()
        self.mashed_routes = dict(((g, a, h), routes[g][a][h]) for g in routes for a in routes[g] for h in routes[g][a])

    @raven_report
    def route(self, IPC_pack):
        session = create_session(bind=self.connect, expire_on_commit=False)

        try:
            Auth_IPC_pack = authorize(IPC_pack, session=session)
            path_parse = Auth_IPC_pack['api_method'].split('/', 4)
            mashed_key = (path_parse[1], path_parse[-1], Auth_IPC_pack['api_type'])
            api_method = self.mashed_routes[mashed_key]

            params = {
                'session': session,
                'query': Auth_IPC_pack['query_params']
            }
            response = api_method(*(path_parse[2:-1]), **params)

        except APIException as e:
            session.rollback()
            return {'error': e.code}

        except Exception as e:
            session.rollback()
            response = {'error': e.message}  # TODO: определить формат ошибок

        finally:
            session.close()

        return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='host', default='127.0.0.1')
    parser.add_argument('--port', dest='port', default=6600)
    parser.add_argument('--testdb', dest='testdb', action='store_true', default=False,
                    help='использование тестовой БД')
    namespace = parser.parse_args()

    if namespace.testdb:
        conf.DATABASE['postgresql'] = conf.DATABASE['test']  # переключение на тестовую БД

    server = zerorpc.Server(ZeroRpcRestApiService())
    server.bind("tcp://{host}:{port}".format(**vars(namespace)))
    print("ZeroRPC: Starting {0} at {host}:{port}".format(ZeroRpcRestApiService.__name__, **vars(namespace)))
    server.run()
