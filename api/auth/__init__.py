# coding: utf-8
from api.auth import login
from api.auth import revoke
from api.auth import session
from api.auth import registration_email
from api.auth import registration_phone

from api.auth.login import post
from api.auth.revoke import revoke
from api.auth.session import get, delete

from api.auth.social_auth.vk_oauth import get as vk_oauth2_get
from api.auth.social_auth.vk_oauth import complete_get as vk_oauth2_complete


routing = (
    # # (r'^login$', {'post': login.post}),
    # # (r'^session$', {'get': session.get, 'delete': session.delete}),
    # # (r'^revoke$', {'get': revoke.revoke}),
    # # (r'^register$', {'post': registration_email.post}),
    # (r'^register_phone$', {'post': registration_phone.post})
    (r'^login/vk-oauth2$', {'get': vk_oauth2_get}),
    (r'^complete/vk-oauth2$', {'get': vk_oauth2_complete}),
)
