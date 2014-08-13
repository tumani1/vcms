# config: utf-8
from raven import Client
from settings import DEBUG


def raven_report(func):
    if DEBUG:
        return func
    else:
        client = Client('http://5aec720be5594c3e8c4e456ec8f8523a:6d461d2eecce47c281c052cff0ec8a63@sentry.aaysm.com:9000/3')

        def rvwrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception, e:
                client.captureException()
        return rvwrapper
