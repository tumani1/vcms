from users_friendship_action import get, post, delete

friendship = {'get': get,
              'post': post,
              'delete': delete,
}


routing = { 'friendship': friendship,
}