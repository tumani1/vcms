import hashlib
import requests
from utils.constants import VK_CLIENT_ID, VK_REDIRECT_URI


def get(auth_user, session, **kwargs):
    url_auth = 'https://api.twitter.com/oauth/request_token'

    md5_first_sig = hashlib.md5()
    first_sig = 'L8ejYRiZZOgUz0jvalLU1xGdm7jwjrrfMJ8U5FtexFQBt74DBx'
    md5_first_sig.update(first_sig)
    md5_first_param = md5_first_sig.hexdigest()

    headers = {
        'realm': 'http%3A%2F%2Fapi.twitter.com%2F',
        'oauth_consumer_key': 'u7Vdu6ScezMQlpcCog3t7g7xx',
        'oauth_signature ': md5_first_param,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_version': '1.0',
    }

    requests.get(url_auth, headers)
    return {'redirect_url': url_auth, 'social': True}


def complete_get(auth_user, session, **kwargs):
    pass
