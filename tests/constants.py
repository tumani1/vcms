# coding: utf-8
import os
import yaml
from settings import BASE_PATH

ZERORPC_SERVICE_URI = "tcp://127.0.0.1:6600"

NODE = {}
with open(os.path.join(BASE_PATH, 'nodeservices', 'configs', 'node_service.yaml')) as conf:
    NODE = yaml.safe_load(conf)