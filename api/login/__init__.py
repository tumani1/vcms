from api.login import vk_oauth
from api.login import fb_oauth
from api.login import odnoklassniki_oauth
from api.login import tw_oauth


routing = (
    (r'^vk-oauth2$', {'get': vk_oauth.get}),
    (r'^complete/vk-oauth2$', {'get': vk_oauth.complete_get}),
    (r'^fb-oauth2$', {'get': fb_oauth.get}),
    (r'^complete/fb-oauth2$', {'get': fb_oauth.complete_get}),
    (r'^ok-oauth2$', {'get': odnoklassniki_oauth.get}),
    (r'^complete/ok-oauth2$', {'get': odnoklassniki_oauth.complete_get}),
    (r'^tw-oauth2$', {'get': tw_oauth.get}),
    (r'^complete/tw-oauth2$', {'get': tw_oauth.complete_get}),

)
