# coding: utf-8
import argparse
import zerorpc
import settings as conf
from api import routes
from api import authorize
from utils.connection import create_session, db_connect, mongo_connect
from zerorpcservice.additional import raven_report


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
            mashed_key = (Auth_IPC_pack['api_group'], Auth_IPC_pack['api_method'], Auth_IPC_pack['http_method'])
            api_method = self.mashed_routes[mashed_key]
            response = api_method(session=session, **Auth_IPC_pack['query_params'])
        except Exception as e:
            session.rollback()
            response = {'error': e.message}  # TODO: определить формат ошибок
        finally:
            session.close()

        return response


class ZeroRpcCdnApiService(object):

    def media_play(self, user_token, media_id):
        return 200

    def media_play_done(self, user_token, media_id):
        return 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='python -m service subcommand [options] [args]')

    subparser = parser.add_subparsers(title='Commands')
    # API zerorpc service
    api_service = subparser.add_parser('api_service', help='Start API zerorpc service')
    api_service.add_argument('--host', dest='host', default='127.0.0.1')
    api_service.add_argument('--port', dest='port', default=6600)
    parser.add_argument('--testdb', dest='testdb', action='store_true', default=False,
                    help='использование тестовой БД')
    api_service.set_defaults(obj=ZeroRpcRestApiService)

    # CDN zerorpc service
    cdn_service = subparser.add_parser('cdn_service', help='Startc CDN zerorpc service')
    cdn_service.add_argument('--host', dest='host', default='127.0.0.1')
    cdn_service.add_argument('--port', dest='port', default=6601)
    cdn_service.set_defaults(obj=ZeroRpcCdnApiService)

    namespace = parser.parse_args()
    server_config = vars(namespace)
    obj_server = server_config.pop('obj')

    if namespace.testdb:
        conf.DATABASE['postgresql'] = conf.DATABASE['test']  # переключение на тестовую БД

    server = zerorpc.Server(obj_server)
    server.bind("tcp://{host}:{port}".format(**server_config))
    print("ZeroRPC: Starting {0} at {host}:{port}".format(namespace.obj.__name__, **server_config))
    server.run()
