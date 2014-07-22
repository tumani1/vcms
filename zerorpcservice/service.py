# coding: utf-8
import argparse
from api import routes
from api import authorize
from utils.connection import create_session, db_connect, mongo_connect
from zerorpcservice.additional import run_zerorpc, raven_report


class ZeroRpcService(object):

    def __init__(self):
        self.connect = db_connect()
        self.mongodb_session = mongo_connect()
        self.mashed_routes = dict(((g, a, h), routes[g][a][h]) for g in routes for a in routes[g] for h in routes[g][a])


    @raven_report
    def route(self, IPC_pack):
        session = create_session(bind=self.connect, expire_on_commit=False)

        try:
            Auth_IPC_pack = authorize(IPC_pack, session=session)
            mashed_key = (Auth_IPC_pack['api_group'], Auth_IPC_pack['api_method'], Auth_IPC_pack['http_method'])
            api_method = self.mashed_routes[mashed_key]
            response = api_method(session=session, **Auth_IPC_pack['query_params'])
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
    namespace = parser.parse_args()
    service_conf = vars(namespace)

    run_zerorpc(ZeroRpcService, service_conf)