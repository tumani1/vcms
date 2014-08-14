from media_list import get as get_list
from media_info import get as get_info
from media_persons import get as get_persons
from media_units import get as get_units
from media_playlist import get as get_playlist, post as post_playlist, delete as delete_playlist
from media_like import get as get_like, post as post_like, delete as delete_like
from media_state import get as get_state, post as post_state, delete as delete_state

routing = (
    ('^list$', {
        'get': get_list
    }),
    ('^(?P<media_id>\d+)/info$', {
        'get': get_info
    }),
    ('^(?P<media_id>\d+)/persons$', {
        'get': get_persons
    }),
    ('^(?P<media_id>\d+)/units$', {
        'get': get_units
    }),
    ('^(?P<media_id>\d+)/playlist$', {
        'get': get_playlist,
        'post': post_playlist,
        'delete': delete_playlist,
    }),
    ('^(?P<media_id>\d+)/like$', {
        'get': get_like,
        'post': post_like,
        'delete': delete_like,
    }),
    ('^(?P<media_id>\d+)/state$', {
        'get': get_state,
        'post': post_state,
        'delete': delete_state,
    }),
)
