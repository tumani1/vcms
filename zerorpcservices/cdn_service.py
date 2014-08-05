# coding: utf-8
import argparse
import zerorpc
import settings as conf
from utils.connection import get_session
from api.cdn import on_done, on_play


class ZeroRpcCdnApiService(object):

    def on_play(self, user_token, media_id):
        session = get_session()
        try:
            params = {
                'auth_user': user_token,
                'session': session,
                'media_id': media_id,
            }
            statuc_code = on_play(**params)
        except Exception as e:
            statuc_code = 500

        return statuc_code

    def on_done(self, user_token, media_id):
        session = get_session()
        try:
            params = {
                'auth_user': user_token,
                'session': session,
                'media_id': media_id,
            }
            statuc_code = on_done(**params)
        except Exception as e:
            statuc_code = 500

        return statuc_code


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='host', default='127.0.0.1')
    parser.add_argument('--port', dest='port', default=6601)
    parser.add_argument('--testdb', dest='testdb', action='store_true', default=False,
                    help='использование тестовой БД')
    namespace = parser.parse_args()

    if namespace.testdb:
        conf.DATABASE['postgresql'] = conf.DATABASE['test']  # переключение на тестовую БД

    server = zerorpc.Server(ZeroRpcCdnApiService())
    server.bind("tcp://{host}:{port}".format(**vars(namespace)))
    print("ZeroRPC: Starting {0} at {host}:{port}".format(ZeroRpcCdnApiService.__name__, **vars(namespace)))
    server.run()