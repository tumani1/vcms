# coding: utf-8
import os
import yaml

DEBUG = False
TEST = True

BASE_PATH = os.path.dirname(__file__)

# Base path for configs folder
CONFIG_PATH = os.path.join(BASE_PATH, 'configs')
GEO_IP_DATABASE = os.path.join(BASE_PATH, 'utils', 'geo_files', 'GeoLite2-Country.mmdb')
CITIES_ZIP_FILE = os.path.join(BASE_PATH, 'utils', 'geo_files', 'cities.zip')
CITIES_FILE = 'cities.csv'

# Parse DB Config
DATABASE = {}
with open(os.path.join(CONFIG_PATH, 'db.yaml'), 'r') as file:
    DATABASE = yaml.load(file, Loader=yaml.loader.Loader)

TOKEN_LIFETIME = 15