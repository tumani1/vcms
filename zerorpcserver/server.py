# coding: utf-8
import zerorpc


class HelloRPC(object):
    def hello(self, s):
        return "{} !!!".format(s.upper())

server = zerorpc.Server(HelloRPC())
server.bind("tcp://0.0.0.0:4242")
server.run()
