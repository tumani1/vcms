from models import db, Users
from utils import need_authorization
from utils.hash_password import hash_pass


@db
@need_authorization
def put(user, password, session=None):
    hashed_password = hash_pass(password)
    user.password = hashed_password
    session.commit()



