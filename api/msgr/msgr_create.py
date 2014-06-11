from models import db
from utils import need_authorization


@db
@need_authorization
def put(user, session=None, **kwargs):
    if kwargs['user_ids'] in None:
        pass