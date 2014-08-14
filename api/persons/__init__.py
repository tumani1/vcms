# coding, utf-8

from persons_info import *
from persons_subscribe import *
from persons_like import *
from persons_extras import *
from persons_values import *
from persons_list import *
from persons_media import *

routing = (
    (r'^list$', {'get': get_person_list}),
    (r'^(?P<id>\d+)/info$', {'get': get_person_info}),
    (r'^(?P<id>\d+)/extras$', {'get': get_person_extars}),
    (r'^(?P<id>\d+)/media$', {'get': get_person_media}),
    (r'^(?P<id>\d+)/values$', {'get': get_person_values}),
    (r'^(?P<id>\d+)/subscribe$', {
        'get': get_subscribe,
        'post': post_subscribe,
        'delete': delete_subscribe,
    }),
    (r'^(?P<id>\d+)/like$', {
        'get': get_like,
        'post': post_like,
        'delete': delete_like,
    }),
)
