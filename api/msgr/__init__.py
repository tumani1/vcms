from api.msgr.msgr_list import get as list_get
from api.msgr.msgr_stat import get as stat_get
from api.msgr.msgr_create import put as create_put
from api.msgr.msgr_info import get as info_get
from api.msgr.msgr_send import put as sent_put
from api.msgr.msgr_stream import get as stream_get

routing = (
    (r'^list$', {
        'get': list_get,
    }),
    (r'^stat$', {
        'get': stat_get,
    }),
    (r'^create$', {
        'put': create_put,
    }),
    (r'^(?P<id>\d+)/info$', {
        'get': info_get
    }),
    (r'^(?P<id>\d+)/send$', {
        'put': sent_put
    }),
    (r'^(?P<id>\d+)/stream$', {
        'get': stream_get
    })
)
