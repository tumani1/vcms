# coding: utf-8
import zerorpc
import yaml
from raven import Client
from api import routes
from api import authorize
from settings import CONFIG_PATH, DEBUG
from os.path import join


mashed_routes = dict(((g, a, h), routes[g][a][h]) for g in routes for a in routes[g] for h in routes[g][a])


def raven_report(func):
    if DEBUG:
        return func
    else:
        client = Client('http://5aec720be5594c3e8c4e456ec8f8523a:6d461d2eecce47c281c052cff0ec8a63@sentry.aaysm.com/3')

        def rvwrapper(IPC_pack):
            try:
                return func(IPC_pack)
            except Exception:
                client.captureException()
        return rvwrapper


class ZeroRpcService(object):

    @raven_report
    def route(self, IPC_pack):
        Auth_IPC_pack = authorize(IPC_pack)
        mashed_key = (Auth_IPC_pack['api_group'], Auth_IPC_pack['api_method'], Auth_IPC_pack['http_method'])
        response = mashed_routes[mashed_key](**Auth_IPC_pack['query_params'])
        return response


def start_zerorpc_service():
    with open(join(CONFIG_PATH, 'zerorpc_service.yaml')) as conf:
        services = yaml.safe_load(conf)

    server = zerorpc.Server(ZeroRpcService())
    server.bind("{schema}://{host}:{port}".format(**services))
    print("zerorpc server runnig on {host}:{port}".format(**services))
    server.run()


if __name__ == '__main__':
    start_zerorpc_service()
