# coding: utf-8
import zerorpc
import ujson
from api import routes
from api import authorize
from raven import Client

DEBUG = True
mashed_routes = dict( ((g,a,h),routes[g][a][h]) for g in routes for a in routes[g] for h in routes[g][a])


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
        pd = ujson.loads(IPC_pack)
        user_id = authorize(pd['token'])
        mashed_key = (pd['api_group'],
                      pd['api_method'],
                      pd['http_method'])
        response = mashed_routes[mashed_key](user_id, **pd['query_params'])
        print(response)
        return response

if __name__ == '__main__':
    server = zerorpc.Server(ZeroRpcService())
    server.bind("tcp://0.0.0.0:4242")
    server.run()
