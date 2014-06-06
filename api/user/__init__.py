from user_info import get, put
from user_values import put as val_put, get as val_get
from user_password import put as password_put
from user_friends import get as friend_get
info = {
    'get': get,
    'put': put
}
values = {'put': val_put, 'get': val_get}
friends = {'get': friend_get}
password = {'put': password_put}
routing = { 'info': info, 'values': values, 'password': password, 'friends': friends }