# coding:utf-8

from api.auth.login import post
from api.auth.revoke import revoke
from api.auth.session import get, delete
from api.auth.registration import post as register


auth = {
    'login': {
        'post': post,
    },
    'session': {
        'get': get,
        'delete': delete,
    },
    'revoke': {
        'get': revoke,
    },
    'register': {
        'post': register,
    }

}
