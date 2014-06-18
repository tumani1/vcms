# coding: utf-8
import os
import sys
import yaml

DEBUG = True

BASE_PATH = os.path.dirname(__file__)

# Base path for configs folder
CONFIG_PATH = os.path.join(BASE_PATH, 'configs')

# Parse DB Config
DATABASE = {}
with open(os.path.join(CONFIG_PATH, 'db.yaml'), 'r') as file:
    DATABASE = yaml.load(file, Loader=yaml.loader.BaseLoader)

if DATABASE['test_config']['use_test_db']:
    PREFIX_TEST = 'test_'
else:
    PREFIX_TEST = ''

if 'true' in sys.argv:
    DATABASE['postgresql']['database'] = PREFIX_TEST + DATABASE['postgresql']['database']
    print DATABASE
TOKEN_LIFETIME = 15

if int(os.environ.get('TEST_EXEC', -1)):
    for k, v in DATABASE.items():
        if 'database' in v:
            v['database'] = PREFIX_TEST + v['database']

