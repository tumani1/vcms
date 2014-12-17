# coding: utf-8

import argparse
import zerorpc
import memcache

import settings as conf
from api import rest_routes
from base_service import BaseService


class ZeroRpcRestApiService(BaseService):

    def __init__(self, *args, **kwargs):
        super(ZeroRpcRestApiService, self).__init__(*args, **kwargs)
        self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='host', default='127.0.0.1')
    parser.add_argument('--port', dest='port', default=6600)
    parser.add_argument('--testdb', dest='testdb', action='store_true', default=False,
                    help='использование тестовой БД')
    namespace = parser.parse_args()

    if namespace.testdb:
        conf.DATABASE['postgresql'] = conf.DATABASE['test']  # переключение на тестовую БД

    server = zerorpc.Server(ZeroRpcRestApiService(rest_routes))
    server.bind("tcp://{host}:{port}".format(**vars(namespace)))
    print("ZeroRPC: Starting {0} at {host}:{port}".format(ZeroRpcRestApiService.__name__, **vars(namespace)))
    server.run()
