# coding=utf-8

from content_info import *
from content_list import *


routing = {
    'list': {
        'get': get_content_list},
    'info': {
        'get': get_content_info}
    }
