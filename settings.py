# coding: utf-8

import os
import yaml

DEBUG = False

BASE_PATH = os.path.dirname(__file__)

# Base path for configs folder
CONFIG_PATH = os.path.join(BASE_PATH, 'configs')

# Parse DB Config
DATABASE = {}
with open(os.path.join(CONFIG_PATH, 'db.yaml'), 'r') as file:
    DATABASE = yaml.load(file, Loader=yaml.loader.Loader)

# Parse Service Config
REST_SERVICE = {}
CDN_SERVICE = {}
with open(os.path.join(CONFIG_PATH, 'zerorpc_service.yaml'), 'r') as conf:
    REST_SERVICE = yaml.safe_load(conf['rest_api'])
    CDN_SERVICE = yaml.safe_load(conf['cdn_api'])


NODE = {}
with open(os.path.join(CONFIG_PATH, 'node_service.yaml'), 'r') as conf:
    NODE = yaml.safe_load(conf)


TOKEN_LIFETIME = 15
