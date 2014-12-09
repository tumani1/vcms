import base64
import hashlib
from urllib import urlencode
import requests
import time

from utils.constants import VK_CLIENT_ID, VK_REDIRECT_URI


def get(auth_user, session, **kwargs):
    url_auth = 'https://api.twitter.com/oauth/request_token'
    ts = time.time()
    sha1_first_sig = hashlib.sha1()
    first_sig = 'L8ejYRiZZOgUz0jvalLU1xGdm7jwjrrfMJ8U5FtexFQBt74DBx&'
    sha1_first_sig.update(first_sig)
    sha1_first_param = sha1_first_sig.hexdigest()


    url = 'https://api.twitter.com/oauth/request_token?oauth_consumer_key=u7Vdu6ScezMQlpcCog3t7g7xx&oauth_signature_method=HMAC-SHA1&' \
          'oauth_timestamp={0}&oauth_version=1.0'.format(ts)
    url = urlencode(url)
    sha1_first_sig.update(url)

    headers = {
        'realm': 'http%3A%2F%2Fapi.twitter.com%2F',
        'oauth_consumer_key': 'u7Vdu6ScezMQlpcCog3t7g7xx',
        'oauth_signature ': base64.b64encode(sha1_first_param),
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': ts,
        'oauth_version': '1.0',
    }

    requests.get(url_auth, headers=headers)
    return {'redirect_url': url_auth, 'social': True}


def complete_get(auth_user, session, **kwargs):
    pass
