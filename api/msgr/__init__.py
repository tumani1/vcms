from api.msgr.msgr_list import get as list_get
from api.msgr.msgr_stat import get as stat_get
from api.msgr.msgr_create import put as create_put

routing = {
    'list': {
        'get': list_get,
    },
    'stat': {
        'get': stat_get,
    },
    'create': {
        'put': create_put,
    }
}
