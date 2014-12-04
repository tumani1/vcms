# coding: utf-8
from api.auth import login
from api.auth import revoke
from api.auth import session
from api.auth import registration_email
from api.auth import registration_phone
from api.login import fb_oauth, vk_oauth


routing = (
    (r'^login$', {'post': login.post}),
    (r'^session$', {'get': session.get, 'delete': session.delete}),
    (r'^revoke$', {'get': revoke}),
    (r'^register$', {'post': registration_email.post}),
    (r'^register_phone$', {'post': registration_phone.post}),
    (r'^login/vk-oauth2$', {'get': vk_oauth.get}),
    (r'^complete/vk-oauth2$', {'get': vk_oauth.complete_get}),
    (r'^login/fb-oauth2$', {'get': fb_oauth.get}),
    (r'^complete/fb-oauth2$', {'get': fb_oauth.complete_get}),

)
