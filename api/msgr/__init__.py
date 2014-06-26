from api.msgr.msgr_list import get as list_get
from api.msgr.msgr_stat import get as stat_get
from api.msgr.msgr_create import put as create_put
from api.msgr.msgr_info import get as info_get
from api.msgr.msgr_sent import put as sent_put
from api.msgr.msgr_stream import get as stream_get

routing = {
    'list': {
        'get': list_get,
    },
    'stat': {
        'get': stat_get,
    },
    'create': {
        'put': create_put,
    },
    'info': {
        'get': info_get
    },
    'sent': {
        'put': sent_put
    },
    'stream': {
        'get': stream_get
    }
}
