from models import db, Users
from utils import need_authorization
from utils.hash_password import hash_password


@db
@need_authorization
def put(user_id, password, session=None):
    user = session.query(Users).filter_by(id=user_id)
    hash = hash_password(password)
    user.password = hash
    session.commit()



