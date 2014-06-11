from models import db, Users
from utils import need_authorization
from utils.hash_password import hash_password


@db
@need_authorization
def put(user, password, session=None):
    hash = hash_password(password)
    user.password = hash
    session.commit()



