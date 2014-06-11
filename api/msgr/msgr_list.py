from models import db
from utils import need_authorization


@db
@need_authorization
def get(user, user_f=None, session=None):
    pass
