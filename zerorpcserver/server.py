# coding: utf-8
import zerorpc

from api import routes
from api import authorize
import ujson
from raven import Client

DEBUG = True

def raven_report(func):
    if DEBUG:
        return func
    else:
        client = Client('http://5aec720be5594c3e8c4e456ec8f8523a:6d461d2eecce47c281c052cff0ec8a63@sentry.aaysm.com/3')
        
        def wrapper(self,json_data):
            try:
                return func(self,json_data)
            except Exception:
                client.captureException()
        return wrapper    


mashed_routes = dict( ((g,a,h),routes[g][a][h]) for g in routes for a in routes[g] for h in routes[g][a])



class HelloRPC(object):
    @raven_report
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
