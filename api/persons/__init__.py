# coding: utf-8

from persons_info import *
from persons_subscribe import *
from persons_like import *
from persons_extras import *
from persons_values import *
from persons_list import *
from persons_media import *

routing = (
    ('^list$', {'get': get_person_list}),
    ('^(?P<person_id>\d+)/info$', {'get': get_person_info}),
    ('^(?P<person_id>\d+)/extras$', {'get': get_person_extars}),
    ('^(?P<person_id>\d+)/media$', {'get': get_person_media}),
    ('^(?P<person_id>\d+)/values$', {'get': get_person_values}),
    ('^(?P<person_id>\d+)/subscribe$', {
        'get': get_subscribe,
        'post': post_subscribe,
        'delete': delete_subscribe,
    }),
    ('^(?P<person_id>\d+)/like$', {
        'get': get_like,
        'post': post_like,
        'delete': delete_like,
    }),
)
