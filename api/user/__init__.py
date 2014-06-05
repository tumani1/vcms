from user_info import get, put
from user_values import put as val_put

info = {
    'get':get,
    'put': put
}
values = {'put': val_put}
routing = { 'info': info, 'values': values
}