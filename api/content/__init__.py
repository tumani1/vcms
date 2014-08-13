# coding=utf-8

from content_info import *
from content_list import *
from content_static import *


routing = {
    'list': {
        'get': get_content_list
    },
    'info': {
        'get': get_content_info
    },
    'users': {
        'get': get_content_users_info
    },
    'persons': {
        'get': get_content_persons_info
    },
    'media': {
        'get': get_content_media_info
    },
    'topics': {
        'get': get_content_topics_info
    },
}
