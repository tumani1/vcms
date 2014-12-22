# coding: utf-8

import argparse
import zerorpc
import settings as conf

from geoip2 import database

from api import internal_routes
from base_service import BaseService


class ZeroRpcInternalApiService(BaseService):

    def __init__(self, *args, **kwargs):
        super(ZeroRpcInternalApiService, self).__init__(*args, **kwargs)
        self.reader_geoip = database.Reader(conf.GEO_IP_DATABASE)
        self.default_params = {
            'reader': self.reader_geoip,
        }

    def route(self, IPC_pack):
        response = super(ZeroRpcInternalApiService, self).route(IPC_pack)
        try:
            self.reader_geoip.close()
        except Exception, e:
            pass

        return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='host', default='127.0.0.1')
    parser.add_argument('--port', dest='port', default=5600)
    parser.add_argument('--testdb', dest='testdb', action='store_true', default=False,
                    help='использование тестовой БД')
    namespace = parser.parse_args()

    if namespace.testdb:
        conf.DATABASE['postgresql'] = conf.DATABASE['test']  # переключение на тестовую БД

    server = zerorpc.Server(ZeroRpcInternalApiService(internal_routes))
    server.bind("tcp://{host}:{port}".format(**vars(namespace)))
    print("ZeroRPC: Starting {0} at {host}:{port}".format(ZeroRpcInternalApiService.__name__, **vars(namespace)))
    server.run()
