from mediaunits_list import get as get_list
from media_units_info import get as get_info

routing = {
    'list': {
        'get': get_list
    },
    'info': {
        'get': get_info
    },
}