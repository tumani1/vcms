import users_friendship_action
import users_info
import users_values
import users_friends
import users_extras
import users_stream

friendship = {'get': users_friendship_action.get,
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

routing = { 'friendship': friendship,
            'info': info,
            'values': values,
            'friends': friends,
            'extras': extras,
            'stream': stream,
}