from obj_comments_create import post as create_obj_comment
from obj_comments_list import get as get_obj_comments_list

routing = (
    (r'^(?P<type>\w+)/(?P<comment>\w+)/list$', {'get': get_obj_comments_list}),
    (r'^(?P<type>\w+)/(?P<comment>\w+)/create$', {'post': create_obj_comment}),
)
