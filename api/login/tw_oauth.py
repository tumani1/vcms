import base64
import hashlib
import random
from urllib import urlencode
from oauthlib.common import unicode_type, generate_timestamp, CaseInsensitiveDict
from oauthlib.oauth1.rfc5849 import signature
from oauthlib.oauth1.rfc5849.parameters import prepare_headers
from oauthlib.oauth1.rfc5849.signature import sign_hmac_sha1
import requests
import time
from requests.utils import to_native_string


def get(auth_user, session, **kwargs):
    url_auth = u'https://api.twitter.com/oauth/request_token'
    url_login = u'https://api.twitter.com/oauth/authenticate?'
    ts = unicode_type(int(time.time()))
    nonce = unicode_type(hashlib.md5(unicode_type(random.getrandbits(64)) + generate_timestamp()))
    collected_params = [
        (u'oauth_callback', u'http://serialov.tv/login/complete/tw-oauth2'),
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
        (u'oauth_callback', u'http://serialov.tv/login/complete/tw-oauth2'),
        (u'oauth_consumer_key', u'u7Vdu6ScezMQlpcCog3t7g7xx'),
        (u'oauth_nonce', nonce),
        (u'oauth_signature', sig),
        (u'oauth_signature_method', u'HMAC-SHA1'),
        (u'oauth_timestamp', ts),
        (u'oauth_version', u'1.0'),

    ]
    headers = prepare_headers(headers)
    # headers = CaseInsensitiveDict((to_native_string(name), value) for name, value in headers.items())
    url = to_native_string(normalized_uri)

    # headers = {
    #     u'oauth_callback': u'http://serialov.tv/login/complete/tw-oauth2',
    #     u'oauth_consumer_key': u'u7Vdu6ScezMQlpcCog3t7g7xx',
    #     u'oauth_nonce': nonce,
    #     u'oauth_signature': sig,
    #     u'oauth_signature_method': u'HMAC-SHA1',
    #     u'oauth_timestamp': ts,
    #     u'oauth_version': u'1.0',
    # }
    #
    # headers = urlencode(headers)
    response = requests.get(url, headers=headers).text
    oauth_token = response.split('&')[0].split('=')[1]
    redirect_url = {'redirect_uri':'http://serialov.tv/login/complete/tw-oauth2'}
    redirect_url = urlencode(redirect_url)
    return {'redirect_url': url_login+redirect_url+'&oauth_token='+oauth_token, 'social': True}


def complete_get(auth_user, session, **kwargs):
    if 'oauth_token' in kwargs:
        oauth_token = kwargs['oauth_token']

    if 'oauth_verifier' in kwargs:
        oauth_verifier = kwargs['oauth_verifier']

    return {'token': oauth_verifier, 'verifier': oauth_verifier}
