from models import db
from models import SessionToken
from utils import need_authorization
from settings import TOKEN_LIFETIME
import datetime

@need_authorization
@db
def get(user,session=None):
    sid, token, created =  SessionToken.generate_token(user.id,session)

    return { 'id': sid,
             'token':token,
             'expire': created + datetime.timedelta(minutes = TOKEN_LIFETIME)
         }
        
@need_authorization
@db
def delete(user,session=None):

    st = session.query(SessionToken).filter(user_id = user.id).first()
    st.is_active = False

    session.add(st)
    session.commit()

    