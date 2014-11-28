# coding: utf-8

from api.auth.login import post
from api.auth.social_auth.vk_oauth import post as vk_oauth2_post
from api.auth.social_auth.vk_oauth import complete_post as vk_oauth2_complete
from api.auth.revoke import revoke
from api.auth.session import get, delete
from api.auth.registration import post as register


routing = (
    (r'^login$', {'post': post}),

    (r'^session$', {'get': get, 'delete': delete}),

    (r'^revoke$', {'get': revoke}),

    (r'^register$', {'post': register}),

    (r'^login/vk-oauth2$',
        {'post': vk_oauth2_post}),

    (r'^complete/vk-oauth2$',
        {'post': vk_oauth2_complete}),


)
