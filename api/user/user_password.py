from models import db, Users
from utils import need_authorization
from utils.hash_password import hash_pass


@db
@need_authorization
def put(auth_user, password, session=None):
    hashed_password = hash_pass(password)
    auth_user.password = hashed_password
    session.commit()



