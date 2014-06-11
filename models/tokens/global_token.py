from models import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date
from models import Base
import os
import base64
import time

def token_gen():
    return base64.b64encode(os.urandom(48),'00')

class GlobalToken(Base):
    __tablename__ = "global_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    token = Column(String(64), default = token_gen )
    created = Column(DateTime, default = time.time())

    @classmethod
    def generate_token(cls,user_id,session = None):
        '''
        (Re)Generate token for given user_id
        '''
        qr = session.query(cls).filter(user_id = user_id).first()

        if qr is None:
            gt = cls(user_id = user_id)
            session.add(gt)
            session.commit()
            return gt.token

        else:
            gt, = qr
            gt.token = token_gen()
            session.add(gt)
            session.commit()
            return gt.token

    @classmethod
    def get_user_id_by_token(cls, token_string, session = None):

        qr = session.query(GlobalToken.user_id).filter(token=token_string).first()

        if qr is None:
            return None
        else:
            return qr[0]
        
            
            
            
            

    


    
        




