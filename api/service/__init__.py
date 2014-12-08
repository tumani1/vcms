# coding: utf-8

from stat import *
from search import *

routing = (
    (r'^search$', {'get': get_search_list}),
    (r'^stat$', {'get': get_stat_list}),
)
