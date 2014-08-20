from items.items_list import get as get_list
from items.items_info import get as get_info
from items.items_variants import get as get_variants

routing = (
    (r'^items/list$', {
        'get': get_list,
    }),
    (r'^items/(?P<media_id>\d+)/info$', {
        'get': get_info,
    }),
    (r'^items/(?P<media_id>\d+)/variants$', {
        'get': get_variants,
    }),
)
