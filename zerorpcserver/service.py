# coding: utf-8
from api import routes
from api import authorize
from utils.connection import create_session, db_connect

import zerorpc
import yaml
from raven import Client
from settings import CONFIG_PATH, DEBUG
from os.path import join


def raven_report(func):
    if DEBUG:
        return func
    else:
        client = Client('http://5aec720be5594c3e8c4e456ec8f8523a:6d461d2eecce47c281c052cff0ec8a63@sentry.aaysm.com/3')

        def rvwrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                client.captureException()
        return rvwrapper


class ZeroRpcService(object):

    def __init__(self):
        self.connect = db_connect()
        self.mashed_routes = dict(((g, a, h), routes[g][a][h]) for g in routes for a in routes[g] for h in routes[g][a])

    @raven_report
    def route(self, IPC_pack):
        response = {}
        session = create_session(bind=self.connect, expire_on_commit=False)

        try:
            Auth_IPC_pack = authorize(IPC_pack, session=session)
            mashed_key = (Auth_IPC_pack['api_group'], Auth_IPC_pack['api_method'], Auth_IPC_pack['http_method'])
            api_method = self.mashed_routes[mashed_key]
            response = api_method(session=session, **Auth_IPC_pack['query_params'])
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        return response

    def __del__(self):
        self.connect.close()


def start_zerorpc_service():
    with open(join(CONFIG_PATH, 'zerorpc_service.yaml')) as conf:
        service = yaml.safe_load(conf)

    server = zerorpc.Server(ZeroRpcService())
    server.bind("{schema}://{host}:{port}".format(**service))
    print("zerorpc server runnig on {host}:{port}".format(**service))
    server.run()


if __name__ == '__main__':
    start_zerorpc_service()
