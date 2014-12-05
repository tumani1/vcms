from api.login import vk_oauth
from api.login import fb_oauth


routing = (
    (r'^vk-oauth2$', {'get': vk_oauth.get}),
    (r'^complete/vk-oauth2$', {'get': vk_oauth.complete_get}),
    (r'^fb-oauth2$', {'get': fb_oauth.get}),
    (r'^complete/fb-oauth2$', {'get': fb_oauth.complete_get}),
)
