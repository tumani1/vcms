from models import db
from models import SessionToken
from utils import need_authorization

@need_authorization
@db
def get(user,session=None):
    return SessionToken.generate_token(user.id,session)
    
        
@need_authorization
@db
def delete(user,session=None):

    session.query(SessionToken).filter(user_id = user.id).first()
    