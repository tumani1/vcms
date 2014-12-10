# coding: utf-8
from os.path import dirname, join
import yaml

DEBUG = False
TEST = True

###########################################################
# Ключи для OAuth2 авторизации
# Vkontakte
SOCIAL_AUTH_VK_OAUTH2_KEY = '4643948'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'qa9kXSjeRTMybQCh6J2I'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email', ]

BASE_PATH = dirname(__file__)
SOCIAL_AVATAR_UPLOAD_DIR = join(BASE_PATH, 'zerorpcservices', 'upload')

# Base path for configs folder
CONFIG_PATH = join(BASE_PATH, 'configs')
GEO_IP_DATABASE = join(BASE_PATH, 'utils', 'geo_files', 'GeoLite2-Country.mmdb')
CITIES_ZIP_FILE = join(BASE_PATH, 'utils', 'geo_files', 'cities.zip')
CITIES_FILE = 'cities.csv'

# Parse DB Config
DATABASE = {}
with open(join(CONFIG_PATH, 'db.yaml'), 'r') as file:
    DATABASE = yaml.load(file, Loader=yaml.loader.Loader)

TOKEN_LIFETIME = 15
