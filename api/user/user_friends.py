from api.users.users_friends import get as users_get_friends
from utils import need_authorization


@need_authorization
def get(auth_user, **kwargs):
    users_get_friends(auth_user.id, **kwargs)
