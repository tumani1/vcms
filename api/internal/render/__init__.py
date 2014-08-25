# coding: utf-8
import auth


routing = (
    (r'^info/session$', {'get': auth.get_user_session}),
    (r'^info/user$', {'get': auth.get_auth_user}),
    (r'^auth/check$', {'get': auth.is_auth}),
)
