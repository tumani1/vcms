from items.items_list import get as get_list

routing = (
    (r'^items/list$', {
        'get': get_list,
    }),
)
