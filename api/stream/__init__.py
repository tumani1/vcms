# coding: utf-8
import stream_info
import stream_like
import stream_list
import stream_stat


info = {
    'get': stream_info.get,
}

list = {
    'get': stream_list.get,
}

like = {
    'get': stream_like.get,
    'post': stream_like.post,
    'delete': stream_like.delete,
}

stat = {
    'get': stream_stat.get,
}


routing = (
    (r'^list$', list),
    (r'^stat$', stat),
    (r'^(?P<id>\d+)/info$', info),
    (r'^(?P<id>\d+)/like$', like)
)
