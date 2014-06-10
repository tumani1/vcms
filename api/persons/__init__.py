# coding: utf-8

from persons_info import *
from persons_subscribe import *
from persons_like import *
from persons_extras import *
from persons_values import *
from persons_list import *
from persons_media import *

routing = {
    'list': {
        'get': get_person_list,
    },
    'info': {
        'get': get_person_info,
    },
    'extras': {
        'get': get_person_extars,
    },
    'media': {
       'get': get_person_media,
    },
    'values': {
        'get': get_person_values,
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
