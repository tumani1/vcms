import hashlib
import random
from urllib import urlencode
from oauthlib.common import unicode_type, generate_timestamp
from oauthlib.oauth1.rfc5849 import signature
from oauthlib.oauth1.rfc5849.parameters import prepare_headers
from oauthlib.oauth1.rfc5849.signature import sign_hmac_sha1
import requests
import time
from requests.utils import to_native_string
from models import UsersSocial, Users, GlobalToken
from models.users.constants import APP_USERS_GENDER_UNDEF, APP_USER_STATUS_ACTIVE, APP_USERSOCIAL_TYPE_TWITTER
from utils import NotAuthorizedException


def get(auth_user, session, **kwargs):
    url_auth = u'https://api.twitter.com/oauth/request_token'
    url_login = u'https://api.twitter.com/oauth/authenticate?'
    ts = unicode_type(int(time.time()))
    nonce = unicode_type(hashlib.md5(unicode_type(random.getrandbits(64)) + generate_timestamp()))
    collected_params = [
        (u'oauth_callback', u'http://serialov.tv/login/complete/tw-oauth'),
        (u'oauth_consumer_key', u'u7Vdu6ScezMQlpcCog3t7g7xx'),
        (u'oauth_nonce', nonce),
        (u'oauth_signature_method', u'HMAC-SHA1'),
        (u'oauth_timestamp', unicode(ts)),
        (u'oauth_version',  u'1.0',)
    ]

    normalized_params = signature.normalize_parameters(collected_params)
    normalized_uri = signature.normalize_base_string_uri(url_auth, None)
    base_string = signature.construct_base_string(u'GET', normalized_uri, normalized_params)
    sig = sign_hmac_sha1(base_string, u'L8ejYRiZZOgUz0jvalLU1xGdm7jwjrrfMJ8U5FtexFQBt74DBx', None)

    headers = [
        (u'oauth_callback', u'http://serialov.tv/login/complete/tw-oauth'),
        (u'oauth_consumer_key', u'u7Vdu6ScezMQlpcCog3t7g7xx'),
        (u'oauth_nonce', nonce),
        (u'oauth_signature', sig),
        (u'oauth_signature_method', u'HMAC-SHA1'),
        (u'oauth_timestamp', ts),
        (u'oauth_version', u'1.0'),

    ]

    headers = prepare_headers(headers)

    url = to_native_string(normalized_uri)

    response = requests.get(url, headers=headers).text
    oauth_token = response.split('&')[0].split('=')[1]
    redirect_url = {'redirect_uri': 'http://serialov.tv/login/complete/tw-oauth'}
    redirect_url = urlencode(redirect_url)
    return {'redirect_url': url_login+redirect_url+'&oauth_token='+oauth_token, 'social': True}


def complete_get(auth_user, session, **kwargs):
    url_auth = u'https://api.twitter.com/oauth/access_token'
    ts = unicode_type(int(time.time()))
    nonce = unicode_type(hashlib.md5(unicode_type(random.getrandbits(64)) + generate_timestamp()))

    params = kwargs['query_params']
    if 'oauth_token' in params:
        oauth_token = unicode(params['oauth_token'])

    if 'oauth_verifier' in params:
        oauth_verifier = unicode(params['oauth_verifier'])

    collected_params = [
        (u'oauth_consumer_key', u'u7Vdu6ScezMQlpcCog3t7g7xx'),
        (u'oauth_nonce', nonce),
        (u'oauth_signature_method', u'HMAC-SHA1'),
        (u'oauth_timestamp', unicode(ts)),
        (u'oauth_verifier', oauth_verifier),
        (u'oauth_version',  u'1.0',)
    ]

    normalized_params = signature.normalize_parameters(collected_params)
    normalized_uri = signature.normalize_base_string_uri(url_auth, None)
    base_string = signature.construct_base_string(u'GET', normalized_uri, normalized_params)

    sig = sign_hmac_sha1(base_string, u'L8ejYRiZZOgUz0jvalLU1xGdm7jwjrrfMJ8U5FtexFQBt74DBx', None)

    headers = [
        (u'oauth_consumer_key', u'u7Vdu6ScezMQlpcCog3t7g7xx'),
        (u'oauth_nonce', nonce),
        (u'oauth_token', oauth_token),
        (u'oauth_verifier', oauth_verifier),
        (u'oauth_signature', sig),
        (u'oauth_signature_method', u'HMAC-SHA1'),
        (u'oauth_timestamp', ts),
        (u'oauth_version', u'1.0'),

    ]
    headers = prepare_headers(headers)
    content = requests.get(url_auth, headers=headers).content
    data = content.split('&')

    if 'oauth_token' in data[0]:
        oauth_token = data[0].split('=')[1]

    if 'oauth_token_secret' in data[1]:
        oauth_token_secret = data[1].split('=')[1]

    if 'user_id' in data[2]:
        user_id = data[2].split('=')[1]

    if 'screen_name' in data[3]:
        screen_name = data[3].split('=')[1]

    users_social = session.query(UsersSocial).filter(UsersSocial.social_user_id == user_id).first()

    if not users_social is None:
        user = session.query(Users).filter(Users.id == users_social.user_id).first()
        return {'token': GlobalToken.generate_token(user.id, session), 'social_token': True}

    try:
        user = Users(firstname=screen_name, lastname='', password=oauth_token_secret,
                     gender=APP_USERS_GENDER_UNDEF, status=APP_USER_STATUS_ACTIVE)

        session.add(user)
        session.commit()
        users_social = UsersSocial(user_id=user.id, sType=APP_USERSOCIAL_TYPE_TWITTER, sToken=' ', social_user_id=user_id)
        session.add(users_social)
        session.commit()
        return {'token': GlobalToken.generate_token(user.id, session), 'social_token': True}

    except Exception as e:
        print(e)
        raise NotAuthorizedException

    # ts = unicode_type(int(time.time()))
    # nonce = unicode_type(hashlib.md5(unicode_type(random.getrandbits(64)) + generate_timestamp()))
    #
    # collected_params = [
    #     (u'oauth_consumer_key', u'u7Vdu6ScezMQlpcCog3t7g7xx'),
    #     (u'oauth_nonce', nonce),
    #     (u'oauth_signature_method', u'HMAC-SHA1'),
    #     (u'oauth_timestamp', unicode(ts)),
    #     (u'oauth_token', unicode(oauth_token)),
    #     (u'oauth_version',  u'1.0'),
    #     (u'screen_name',  unicode(screen_name))
    # ]
    #
    # normalized_params = signature.normalize_parameters(collected_params)
    #
    # base_string = signature.construct_base_string(u'GET', u'https://api.twitter.com/1.1/users/show.json', normalized_params)
    # key = u'L8ejYRiZZOgUz0jvalLU1xGdm7jwjrrfMJ8U5FtexFQBt74DBx&' + unicode(oauth_token_secret)
    # sig = sign_hmac_sha1(base_string, key, None)
    #
    # headers = {
    #     u'oauth_consumer_key': u'u7Vdu6ScezMQlpcCog3t7g7xx',
    #     u'oauth_nonce': nonce,
    #     u'oauth_signature': sig,
    #     u'oauth_signature_method': u'HMAC-SHA1',
    #     u'oauth_timestamp': unicode(ts),
    #     u'oauth_token': unicode(oauth_token),
    #     u'oauth_version': u'1.0',
    #     u'screen_name': unicode(screen_name)
    # }
    # headers = urlencode(headers)
    # response = requests.get(u'https://api.twitter.com/1.1/users/show.json?'+headers)
    #
    # return {'text': response.json()}
