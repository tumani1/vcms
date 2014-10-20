# coding: utf-8
from api.auth.login import post
from api.auth.revoke import revoke
from api.auth.session import get, delete
from api.auth.registration_email import post as register
from api.auth import registration_phone


routing = (
    (r'^login$', {'post': post}),
    (r'^session$', {'get': get, 'delete': delete}),
    (r'^revoke$', {'get': revoke}),
    (r'^register$', {'post': register}),
    (r'^register_phone$', {'post': registration_phone.post})
)
