from items.items_list import get as get_list
from items.items_info import get as get_info
from items.items_variants import get as get_variants
from items.items_extras import get as get_extras
from categories.categories_info import get as get_categories_info
from categories.categories_list import get as get_categories_list
from categories.categories_extras import get as get_categories_extras
from categories.categories_items import get as get_categories_items
from items.items_book import post as post_book_item, delete as delete_book_item
from items.items_objects import get as get_objects
from cart.cart_stat import get as get_cart_stat
from cart.cart_items import get as get_cart_items

routing = (
    (r'^items/list$', {
        'get': get_list,
    }),
    (r'^items/(?P<item_id>\d+)/info$', {
        'get': get_info,
    }),
    (r'^items/(?P<item_id>\d+)/variants$', {
        'get': get_variants,
    }),
    (r'^items/(?P<item_id>\d+)/extras$', {
        'get': get_extras,
    }),
    (r'^items/(?P<item_id>\d+)/objects$', {
        'get': get_objects,
    }),
    (r'^items/(?P<item_id>\d+)/book$', {
        'post': post_book_item,
        'delete': delete_book_item,
    }),
    (r'^categories/(?P<categories_id>\d+)/info$', {
        'get': get_categories_info,
    }),
    (r'^categories/list$', {
        'get': get_categories_list,
    }),
    (r'^categories/(?P<categories_id>\d+)/extras$', {
        'get': get_categories_extras,
    }),
    (r'^categories/(?P<categories_id>\d+)/items$', {
        'get': get_categories_items,
    }),
    (r'^cart/stat$', {
        'get': get_cart_stat,
    }),
    (r'^cart/items$', {
       'get': get_cart_items,
    }),
)
