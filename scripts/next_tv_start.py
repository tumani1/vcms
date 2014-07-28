#coding: utf-8

import argparse

import settings as conf
from zerorpcservice.additional import run_zerorpc
from zerorpcservice.service import ZeroRpcRestApiService


parser = argparse.ArgumentParser(description='Start NextTV service')
parser.add_argument('-t', '--test', dest='test', action='store_true', default=False,
                    help='Run server with test params')
args = parser.parse_args()

if args.test:
    conf.DATABASE['postgresql'] = conf.DATABASE['test']

# Start ZeroRPC Service
run_zerorpc(ZeroRpcRestApiService, conf.REST_SERVICE)
