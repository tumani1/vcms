from mediaunits_list import get as get_list
from mediaunits_info import get as get_info
from mediaunits_prev import get as get_prev
from mediaunits_next import get as get_next
from mediaunits_media import get as get_media

routing = {
    'list': {
        'get': get_list
    },
    'info': {
        'get': get_info
    },
    'prev': {
        'get': get_prev
    },
    'next': {
        'get': get_next
    },
    'media': {
        'get': get_media
    }
}