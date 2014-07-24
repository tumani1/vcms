from obj_comments_create import post as create_obj_comment
from obj_comments_list import get as get_obj_comments_list

routing = {
    'list': {
        'get': get_obj_comments_list,
    },
    'create': {
        'post': create_obj_comment,
    },
}
