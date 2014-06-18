from models import db
from models import SessionToken
from utils import need_authorization
from settings import TOKEN_LIFETIME
import datetime
from utils.serializer import serialize
@need_authorization
@serialize
@db
def get(auth_user,session=None, **kwargs):
    sid, token, created =  SessionToken.generate_token(auth_user.id,session)

    result = { 'id': sid,
             'session_token':token,
             'expire': created + datetime.timedelta(minutes = TOKEN_LIFETIME)
         }
    return result
        
@need_authorization
@db
def delete(auth_user,session=None, **kwargs):

    st = session.query(SessionToken).filter(SessionToken.user_id == auth_user.id).first()
    st.is_active = False

    session.add(st)
    session.commit()

    