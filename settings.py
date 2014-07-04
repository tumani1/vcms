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
SERVICE = {}
with open(os.path.join(CONFIG_PATH, 'zerorpc_service.yaml')) as conf:
    SERVICE = yaml.safe_load(conf)

TOKEN_LIFETIME = 15
