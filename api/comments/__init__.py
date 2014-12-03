# coding: utf-8
from comments_list import get as get_list
from comments_info import get as get_info
from comments_like import put as put_like, delete as delete_like
from comments_create import post as post_comment, delete as delete_comment
from comments_reply import post as post_reply

routing = (
    (r'^list$', {
        'get': get_list
    }),
    (r'^(?P<comment_id>\d+)/info$', {
        'get': get_info
    }),
    (r'^(?P<comment_id>\d+)/like$', {
        'put': put_like,
        'delete': delete_like
    }),
    (r'^create$', {
        'post': post_comment,
        'delete': delete_comment
    }),
    (r'^(?P<parent_id>\d+)/reply$', {
        'post': post_reply,
    }),
)
