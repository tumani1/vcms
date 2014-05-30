# coding: utf-8
import os
from ConfigParser import RawConfigParser

BASE_PATH = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(BASE_PATH)
CONFIG_PATH = os.path.join(BASE_DIR, 'configs')

ENGINE_STR_TPL = '{engine}://{username}:{password}@{host}:{port}/{database}'

database_config = RawConfigParser()
database_config.read(os.path.join(CONFIG_PATH, 'db.ini'))

DATABASE = {
    'engine': database_config.get('database', 'ENGINE'),
    'username': database_config.get('database', 'USERNAME'),
    'password': database_config.get('database', 'PASSWORD'),
    'host': database_config.get('database', 'HOST'),
    'port': database_config.get('database', 'PORT'),
    'database': database_config.get('database', 'DATABASE'),
}

ENGINE_STR = ENGINE_STR_TPL.format(**DATABASE)