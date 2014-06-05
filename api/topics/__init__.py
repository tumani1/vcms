# coding: utf-8

from topics_info import *
from topics_list import *
from topics_extras import *


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
}
