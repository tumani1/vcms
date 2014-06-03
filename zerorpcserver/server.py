# coding: utf-8
import zerorpc


class HelloRPC(object):
    def routing(self, json_data):
        return "{}".format(json_data)

server = zerorpc.Server(HelloRPC())
server.bind("tcp://0.0.0.0:4242")
server.run()
