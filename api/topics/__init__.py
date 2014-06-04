# coding: utf-8

from topics_info import get_topics_info
from topics_list import get_topics_list

routing = {
    'info': {
        'get': get_topics_info,
    },
    'list': {
        'get': get_topics_list,
    },
}
