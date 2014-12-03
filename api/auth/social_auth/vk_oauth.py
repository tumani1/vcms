# coding: utf-8
from requests import request
import requests
from models import Users, UsersSocial, GlobalToken
from models.users.constants import APP_USERSOCIAL_TYPE_VK
from utils.constants import VK_SECRET_KEY, VK_CLIENT_ID, VK_REDIRECT_URI


def get(auth_user, session, **kwargs):

    if 'meta' in kwargs:
        meta = kwargs['meta']

    url_auth = 'https://oauth.vk.com/authorize' \
               '?client_id={client_id}' \
               '&scope={scope}' \
               '&redirect_uri={redirect}' \
               '&response_type=code'

    url_auth = url_auth.format(client_id=VK_CLIENT_ID, scope='email', redirect=VK_REDIRECT_URI)
    return url_auth


def complete_get(auth_user, session,**kwargs):
    params = kwargs['query_params']

    if 'code' in params:
        code = params['code']

    url = 'https://oauth.vk.com/access_token' \
          '?client_id={id}' \
          '&client_secret={secret}' \
          '&code={code}' \
          '&redirect_uri={uri}'

    url = url.format(id=VK_CLIENT_ID, secret=VK_SECRET_KEY, code=code, uri=VK_REDIRECT_URI)
    response = requests.get(url)
    data = response.json()

    vk_params = {
        'params': {
            'access_token': data['access_token'],
            'fields': 'first_name,last_name,screen_name,photo,photo_max_orig,nickname',
            'uids': data['user_id']
        }
    }

    method = 'GET'
    url_vk_api = 'https://api.vk.com/method/users.get'

    data_user = request(method, url_vk_api, **vk_params).json()['response'][0]
    user = Users(firstname=data_user['first_name'], lastname=data_user['last_name'], email='aasasdsdzxc@mail.ru', city_id=1, password=data['access_token'])
    session.add(user)
    session.commit()

    users_social = UsersSocial(user_id=user.id, sType=APP_USERSOCIAL_TYPE_VK, sToken='asd')
    session.add(users_social)
    session.commit()

    return {'token': GlobalToken.generate_token(user.id, session)}





