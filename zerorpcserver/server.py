# coding: utf-8
import zerorpc
import ujson
from api import routes
from api import authorize

mashed_routes = dict( ((g,a,h),routes[g][a][h]) for g in routes for a in routes[g] for h in routes[g][a])


class ZeroRpcService(object):

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