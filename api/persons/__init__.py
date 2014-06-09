# coding: utf-8

from persons_info import *
from persons_subscribe import *
from persons_like import *

routing = {
    'info': {
        'GET': get_person_info,
    },
    'subscribe': {
        'get': get_subscribe,
        'post': post_subscribe,
        'delete': delete_subscribe,
    },
    'like': {
        'get': get_like,
        'post': post_like,
        'delete': delete_like,
    },
}
