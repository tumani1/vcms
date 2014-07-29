# coding: utf-8
import os
import yaml

DEBUG = False

BASE_PATH = os.path.dirname(__file__)

# Parse DB Config
DATABASE = {
    'postgresql': {
        'drivername': 'postgresql+psycopg2',
        'username': 'pgadmin',
        'password': 'qwerty',
        'host': 'localhost',
        'port': 5432,
        'database': 'next_tv'},

    'test': {
        'drivername': 'postgresql+psycopg2',
        'username': 'pgadmin',
        'password': 'qwerty',
        'host': 'localhost',
        'port': 5432,
        'database': 'test_next_tv'},

    'mongodb': {
        'db': 'next_tv',
        'username': 'admin',
        'password': 'admin',
        'host': '127.0.0.1',
        'port': 27017}
}

NODE = {}
with open(os.path.join(BASE_PATH, 'nodeservices', 'configs', 'node_service.yaml')) as conf:
    NODE = yaml.safe_load(conf)

TOKEN_LIFETIME = 15