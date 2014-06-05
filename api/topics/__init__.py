# coding: utf-8

from topics_info import *
from topics_list import *
from topics_extras import *
from topics_values import *
from topics_subscribe import *
from topics_like import *


routing = {
    'info': {
        'get': get_topic_info,
    },
    'list': {
        'get': get_topics_list,
    },
    'extras': {
        'get': get_topic_extars,
    },
    'values': {
        'get': get_topic_values,
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
