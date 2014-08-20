from items.items_list import get as get_list
from categories.categories_info import get as get_categories_list

routing = (
    (r'^items/list$', {
        'get': get_list,
    }),
    (r'^categories/(?P<categories_id>\d+)/info$', {
        'get': get_categories_list,
    }),
)
