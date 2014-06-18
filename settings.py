# coding: utf-8
import os
import sys
import yaml

DEBUG = True

BASE_PATH = os.path.dirname(__file__)

# Base path for configs folder
CONFIG_PATH = os.path.join(BASE_PATH, 'configs')
PREFIX_TEST = 'test_'

# Parse DB Config
DATABASE = {}
with open(os.path.join(CONFIG_PATH, 'db.yaml'), 'r') as file:
    DATABASE = yaml.load(file, Loader=yaml.loader.BaseLoader)

if 'true' in sys.argv:
    DATABASE['postgresql']['database'] = PREFIX_TEST + DATABASE['postgresql']['database']
    print DATABASE
TOKEN_LIFETIME = 15

PREFIX_TEST = "test_"

if int(os.environ.get('TEST_EXEC', -1)):
    for k, v in DATABASE.items():
        v['database'] = PREFIX_TEST + v['database']

