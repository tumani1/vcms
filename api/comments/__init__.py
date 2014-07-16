from comments_list import get as get_list
from comments_info import get as get_info
from comments_like import put as put_like, delete as delete_like
from comments_create import post as post_comment, delete as delete_comment

routing = {
    'list': {
        'get': get_list
    },
    'info': {
        'get': get_info
    },
    'like': {
        'put': put_like,
        'delete': delete_like
    },
    'create': {
        'post': post_comment,
        'delete': delete_comment
    },
}
