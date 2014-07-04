# coding: utf-8
import stream_info
import stream_like
import stream_list


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


routing = {
    'list': list,
    'info': info,
    'like': like,
}
