# coding: utf-8
from api.news.news_list import get as list_get
from api.news.news_info import get as info_get
from api.news.news_comments import get as comments_get, post as comments_add

routing = (
    (r'^list$', {
        'get': list_get,
    }),
    (r'^(?P<news_id>\d+)/info$', {
        'get': info_get
    }),
    (r'^(?P<news_id>\d+)/comments$', {
        'get': comments_get
    }),
    (r'^(?P<news_id>\d+)/add_comment$', {
        'post': comments_add
    }),
)
