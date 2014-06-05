from user_info import get
from user_password import put as password_put
info = {'get':get
}

password = {'put':password_put
}
routing = { 'info': info,
            'password': password,
}