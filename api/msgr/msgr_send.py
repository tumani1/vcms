from db_engine import db
from utils import need_authorization


@db
@need_authorization
def put(auth_user, session, **kwargs):
    pass
