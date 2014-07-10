from media_list import get as get_list
from media_info import get as get_info
from media_persons import get as get_persons
from media_units import get as get_units
from media_playlist import get as get_playlist, post as post_playlist, delete as delete_playlist
from media_like import get as get_like, post as post_like, delete as delete_like
from media_state import get as get_state, post as post_state, delete as delete_state

routing = {
    'list': {
        'get': get_list
    },
    'info': {
        'get': get_info
    },
    'persons': {
        'get': get_persons
    },
    'units': {
        'get': get_units
    },
    'playlist': {
        'get': get_playlist,
        'post': post_playlist,
        'delete': delete_playlist,
    },
    'like': {
        'get': get_like,
        'post': post_like,
        'delete': delete_like,
    },
    'state': {
        'get': get_state,
        'post': post_state,
        'delete': delete_state,
    },

}
