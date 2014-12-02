# coding: utf-8

from api.auth.login import post
from api.auth.social_auth.vk_oauth import get as vk_oauth2_get
from api.auth.social_auth.vk_oauth import complete_get as vk_oauth2_complete
from api.auth.revoke import revoke
from api.auth.session import get, delete
from api.auth.registration import post as register


routing = (
    (r'^login$', {'post': post}),

    (r'^session$', {'get': get, 'delete': delete}),

    (r'^revoke$', {'get': revoke}),

    (r'^register$', {'post': register}),

    (r'^login/vk-oauth2$',
        {'get': vk_oauth2_get}),

    (r'^complete/vk-oauth2$',
        {'get': vk_oauth2_complete}),


)
