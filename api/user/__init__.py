# coding: utf-8
from user_info import get, put
from user_values import put as val_put, get as val_get
from user_password import put as password_put
from user_friends import get as friend_get

routing = (
    (r'^info$', {'get': get, 'put': put}),
    (r'^values$', {'put': val_put, 'get': val_get}),
    (r'^password$', {'put': password_put}),
    (r'^friends$', {'get': friend_get}),
)
