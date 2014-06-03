import zerorpc


class ZeroRpcService(object):

    def route(self, IPC_pack):
        print("received from nodejs {}".format(IPC_pack))
        return "from zerorpc service {}".format(IPC_pack)


s = zerorpc.Server(ZeroRpcService())
s.bind("tcp://0.0.0.0:4242")
s.run()