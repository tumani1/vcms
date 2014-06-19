from db_engine import db
from utils import need_authorization


@db
@need_authorization
def put(user, session, **kwargs):
    pass
