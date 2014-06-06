def put(user_id, **kwargs):
    return kwargs

def get(user_id, **kwargs):
    return kwargs

routes = {'echo':
            {'PUT': put,
             'GET': get}
}