from utils.constants import VK_CLIENT_ID, VK_REDIRECT_URI


def get(auth_user, session, **kwargs):
    url_auth = 'https://api.twitter.com/oauth/request_token'
    headers = {
        'realm': 'http%3A%2F%2Fapi.twitter.com%2F',
        'oauth_consumer_key': 'u7Vdu6ScezMQlpcCog3t7g7xx',
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': '137131200',
        'oauth_nonce' : '4572616e48616d6d65724c61686176',
        'oauth_version': '1.0',
        'oauth_signature': 'wOJIO9A2W5mFwDgiDvZbTSMK%2FPY%3D'

    }

    url_auth = url_auth.format(client_id=VK_CLIENT_ID, scope='email', redirect=VK_REDIRECT_URI)
    return {'redirect_url': url_auth, 'social': True}


def complete_get(auth_user, session, **kwargs):
    pass
