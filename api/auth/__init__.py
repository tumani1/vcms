from api.auth.login import post
from api.auth.revoke import revoke
from api.auth.session import get,delete


auth = {'login':
        {'post':post},
        'session':{
            'get':get,
  'delete':delete},
 'revoke':{'get':revoke}
    }
