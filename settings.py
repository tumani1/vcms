# coding: utf-8
import os
import yaml

DEBUG = False

###########################################################
# Ключи для OAuth2 авторизации
# Vkontakte
SOCIAL_AUTH_VK_OAUTH2_KEY = '4643948'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'qa9kXSjeRTMybQCh6J2I'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email', ]

BASE_PATH = os.path.dirname(__file__)

# Base path for configs folder
CONFIG_PATH = os.path.join(BASE_PATH, 'configs')
GEO_IP_DATABASE = os.path.join(BASE_PATH, 'GeoLite2-Country.mmdb')

# Parse DB Config
DATABASE = {}
with open(os.path.join(CONFIG_PATH, 'db.yaml'), 'r') as file:
    DATABASE = yaml.load(file, Loader=yaml.loader.Loader)

TOKEN_LIFETIME = 15
