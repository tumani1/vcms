# coding: utf-8

import zerorpc
import yaml
from raven import Client
from api import routes
from api import authorize


DEBUG = True
mashed_routes = dict(((g, a, h), routes[g][a][h]) for g in routes for a in routes[g] for h in routes[g][a])


def raven_report(func):
    if DEBUG:
        return func
    else:
        client = Client('http://5aec720be5594c3e8c4e456ec8f8523a:6d461d2eecce47c281c052cff0ec8a63@sentry.aaysm.com/3')

        def wrapper(self, IPC_pack):
            try:
                return func(self, IPC_pack)
            except Exception:
                client.captureException()
        return wrapper


class ZeroRpcService(object):

    @raven_report
    def route(self, IPC_pack):
        print(IPC_pack)
        user_id = authorize(IPC_pack['token'])
        mashed_key = (IPC_pack['api_group'], IPC_pack['api_method'], IPC_pack['http_method'])
        response = mashed_routes[mashed_key](user_id, **IPC_pack['query_params'])
        return response


if __name__ == '__main__':
    with open('../configs/zero_rpc_services.yaml') as conf:
        services = yaml.safe_load(conf)

    for s in services:
        server = zerorpc.Server(ZeroRpcService())
        server.bind("{schema}://{address}:{port}".format(**s))
        server.run()
