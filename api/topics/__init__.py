# coding: utf-8
from topics_info import *
from topics_list import *
from topics_extras import *
from topics_values import *
from topics_subscribe import *
from topics_like import *
from topics_persons import *
from topics_media import *


routing = (
    (r'^list$', {'get': get_topics_list}),
    (r'^(?P<name>\w+)/info$', {'get': get_topic_info}),
    (r'^(?P<name>\w+)/extras$', {'get': get_topic_extars}),
    (r'^(?P<name>\w+)/persons$', {'get': get_topic_person}),
    (r'^(?P<name>\w+)/media$', {'get': get_topic_media}),
    (r'^(?P<name>\w+)/values$', {'get': get_topic_values}),
    (r'^(?P<name>\w+)/subscribe$', {
        'get': get_subscribe,
        'post': post_subscribe,
        'delete': delete_subscribe}),
    (r'^(?P<name>\w+)/like$', {
        'get': get_like,
        'post': post_like,
        'delete': delete_like}),
)
