#coding: utf-8

import argparse

import settings as conf
from utils.service import make_zerorpc
from zerorpcserver.service import ZeroRpcService


def main():
    parser = argparse.ArgumentParser(description='Start NextTV service')
    parser.add_argument('-t', '--test', dest='test', action='store_true',
                        default=False, help='Run server with test params')
    args = parser.parse_args()

    if args.test:
        conf.DATABASE['postgresql'] = conf.DATABASE['test']

    # Start ZeroRPC Service
    make_zerorpc(ZeroRpcService, conf.SERVICE)


if __name__ == '__main__':
    main()