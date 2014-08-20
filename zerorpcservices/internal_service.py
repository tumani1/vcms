# coding: utf-8
import argparse
import zerorpc
from geoip2 import database

import settings as conf
from api import cdn_routes
from base_service import BaseService


class ZeroRpcInternalApiService(BaseService):

    def __init__(self, routes):
        super(ZeroRpcInternalApiService, self).__init__(routes)
        self.reader_geoip = database.Reader(conf.GEO_IP_DATABASE)
        self.default_params = {'reader': self.reader_geoip, }

    def __del__(self):
        self.reader_geoip.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='host', default='127.0.0.1')
    parser.add_argument('--port', dest='port', default=6600)
    parser.add_argument('--testdb', dest='testdb', action='store_true', default=False,
                    help='использование тестовой БД')
    namespace = parser.parse_args()

    if namespace.testdb:
        conf.DATABASE['postgresql'] = conf.DATABASE['test']  # переключение на тестовую БД

    server = zerorpc.Server(ZeroRpcInternalApiService(cdn_routes))
    server.bind("tcp://{host}:{port}".format(**vars(namespace)))
    print("ZeroRPC: Starting {0} at {host}:{port}".format(ZeroRpcInternalApiService.__name__, **vars(namespace)))
    server.run()