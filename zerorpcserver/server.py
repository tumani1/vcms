# coding: utf-8
import zerorpc

from api import routes
from api import authorize
import ujson

mashed_routes = dict( ((g,a,h),routes[g][a][h]) for g in routes for a in routes[g] for h in routes[g][a])

class HelloRPC(object):
    def routing(self, json_data):

        pd = ujson.loads(json_data)

        user_id = authorize(pd['token'])

        mashed_key = (pd['api_group'],
                      pd['api_method'],
                      pd['http_method'])
                      
        
        #response = routes[pd['api_group']][pd['api_method']][pd['http_method']](user_id = user_id,**pd['query_params'])
        response = mashed_routes[mashed_key](user_id,**pd['query_params'])
        
        return response

server = zerorpc.Server(HelloRPC())
server.bind("tcp://0.0.0.0:4242")
server.run()
