from user_info import get, put
from user_values import put as val_put
from user_password import put as password_put
info = {
    'get':get,
    'put': put
}
values = {'put': val_put}
password = {'put':password_put}
routing = { 'info': info, 'values': values, 'password': password,
}