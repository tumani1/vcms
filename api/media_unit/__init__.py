# coding: utf-8
from mediaunits_list import get as get_list
from mediaunits_info import get as get_info
from mediaunits_prev import get as get_prev
from mediaunits_next import get as get_next
from mediaunits_media import get as get_media
from mediaunits_like import get as get_like, post, delete


routing = (
    (r'^list$', {'get': get_list}),
    (r'^(?P<id>\d+)/like$', {'get': get_like, 'post': post, 'delete': delete}),
    (r'^(?P<id>\d+)/info$', {'get': get_info}),
    (r'^(?P<id>\d+)/prev$', {'get': get_prev}),
    (r'^(?P<id>\d+)/next$', {'get': get_next}),
    (r'^(?P<id>\d+)/media$', {'get': get_media}),
)

