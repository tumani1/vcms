# coding: utf-8

from content_info import *
from content_list import *
from content_static import *


routing = (
    (r'^list$', {'get': get_content_list}),
    (r'^(?P<id>\d+)/info$', {'get': get_content_info}),
    (r'^users/(?P<pk>\d+)/.*$', {'get': get_content_users_info}),
    (r'^persons/(?P<pk>\d+)/.*$', {'get': get_content_persons_info}),
    (r'^media/(?P<pk>\d+)/.*$', {'get': get_content_media_info}),
    (r'^mediaunit/(?P<pk>\d+)/.*$', {'get': get_content_mediaunits_info}),
    (r'^topics/(?P<pk>\d+)/.*$', {'get': get_content_topics_info}),
)
