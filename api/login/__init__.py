from api.login import vk_oauth
from api.login import fb_oauth


routing = (
    (r'^login/vk-oauth2$', {'get': vk_oauth.get}),
    (r'^complete/vk-oauth2$', {'get': vk_oauth.complete_get}),
    (r'^login/fb-oauth2$', {'get': fb_oauth.get}),
    (r'^complete/fb-oauth2$', {'get': fb_oauth.complete_get}),
)
