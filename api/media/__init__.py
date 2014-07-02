from media_list import get as get_list
from media_info import get as get_info
from media_persons import get as get_persons
routing = {
    'list': {
        'get': get_list
    },
    'info': {
        'get': get_info
    },
    'persons': {
        'get': get_persons
    }
}
