# coding: utf-8
from api.auth.login import post
from api.auth.revoke import revoke
from api.auth.session import get, delete
from api.auth.registration import post as register


routing = (
    (r'^login$', {'post': post}),
    (r'^session$', {'get': get, 'delete': delete}),
    (r'^revoke$', {'get': revoke}),
    (r'^register$', {'post': register})
)
