from social.backends.utils import get_backend
from social.exceptions import MissingBackend
from social.utils import module_member


def get_strategy(strategy, storage, session, request=None, backend=None,
                 *args, **kwargs):
    backends = ('social.backends.vk.VKOAuth2',
                'social.backends.google.GoogleOAuth2',
                'social.backends.facebook.FacebookOAuth2',
                'social.backends.twitter.TwitterOAuth')
    if backend:
        Backend = get_backend(backends, backend)
        if not Backend:
            raise MissingBackend(backend)
    else:
        Backend = None
    Strategy = module_member(strategy)
    Storage = module_member(storage)
    return Strategy(Storage, session, backends, Backend, request, *args, **kwargs)


