# coding: utf-8

from utils.strategy import get_strategy


def post(auth_user, session, **kwargs):
    if 'meta' in kwargs:
        meta = kwargs['meta']
    storage = 'social.storage.sqlalchemy_orm.BaseSQLAlchemyStorage'
    backend = u'vk-oauth2'
    strategy = 'api.auth.social_auth.AuthStrategy.AuthStrategy'
    request = {
        'data': {
            'next': [u'/tokenize/?back_utl=/']
        },
        'hosts': meta['ip_address']

    }
    strategy = get_strategy(strategy, storage, backend=backend, request=request)


    do_auth(strategy)


def complete_post():
    pass


def do_auth(strategy, redirect_name='next'):

    data = strategy.request_data(merge=True)

    if redirect_name in data:
        redirect_uri = data[redirect_name]

        strategy.session_set(
            redirect_name,
            redirect_uri
        )
    return strategy.start()

