# coding: utf-8
from users import routing as users_routing
from topics import routing as topics_routing
from persons import routing as persons_routing

routes = {
    'users': users_routing,
    'topics': topics_routing,
    'persons' : persons_routing
}

def authorize(token):

    if token=='foobar':
        return 1
    elif token == 'snafu':
        return 2
    else:
        return None

    