# coding: utf-8

from content_info import *
from content_list import *
from content_static import *


routing = (
    ('^list$', {'get': get_content_list}),
    ('^(?P<id>\d+)/info$', {'get': get_content_info}),
    ('^users/(?P<pk>\d+)/.*$', {'get': get_content_users_info}),
    ('^persons/(?P<pk>\d+)/.*$', {'get': get_content_persons_info}),
    ('^media/(?P<pk>\d+)/.*$', {'get': get_content_media_info}),
    ('^mediaunit/(?P<pk>\d+)/.*$', {'get': get_content_mediaunits_info}),
    ('^topics/(?P<pk>\d+)/.*$', {'get': get_content_topics_info}),
)
