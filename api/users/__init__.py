# coding: utf-8
import users_friendship_action
import users_info
import users_values
import users_friends
import users_extras
import users_stream
import users_list
import users_black_list_action

friendship = {
    'get': users_friendship_action.get,
    'post': users_friendship_action.post,
    'delete': users_friendship_action.delete,
}

info = {
    'get': users_info.get,
}

values = {
    'get': users_values.get,
}

friends = {
    'get': users_friends.get
}

extras = {
    'get': users_extras.get
}

stream = {
    'get': users_stream.get
}

list = {
    'get': users_list.get,
}

blacklist = {
    'post': users_black_list_action.post,
    'delete': users_black_list_action.delete,
}

routing = (
    (r'^list$', list),
    (r'^(?P<user_id>\d+)/info$', info),
    (r'^(?P<user_id>\d+)/friends$', friends),
    (r'^(?P<user_id>\d+)/values$', values),
    (r'^(?P<user_id>\d+)/extras$', extras),
    (r'^(?P<user_id>\d+)/stream', stream),
    (r'^(?P<user_id>\d+)/friendship', friendship),
    (r'^(?P<user_id>\d+)/blacklist$', blacklist),
)
