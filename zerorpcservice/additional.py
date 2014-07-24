# config: utf-8
import yaml
import zerorpc
from os.path import join
from raven import Client
from settings import CONFIG_PATH, DEBUG


def run_zerorpc(cls, service_conf=None):
    if service_conf is None:
        with open(join(CONFIG_PATH, 'zerorpc_service.yaml')) as conf:
            service_conf = yaml.safe_load(conf)

    server = zerorpc.Server(cls())
    server.bind("tcp://{host}:{port}".format(**service_conf))
    print("ZeroRPC: Starting {0} at {host}:{port}".format(cls.__name__, **service_conf))
    server.run()


def raven_report(func):
    if DEBUG:
        return func
    else:
        client = Client('http://5aec720be5594c3e8c4e456ec8f8523a:6d461d2eecce47c281c052cff0ec8a63@sentry.aaysm.com/3')

        def rvwrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception, e:
                client.captureException()
        return rvwrapper
