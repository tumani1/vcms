#coding: utf-8
from token import TokenMixin


class GlobalToken(TokenMixin):
    __tablename__ = "global_tokens"

    @classmethod
    def get_user_id_by_token(cls, token_string, session=None):

        qr = session.query(GlobalToken.user_id).filter(cls.token == token_string).first()

        if qr is None:
            return None
        else:
            return qr
        
            
            
            
            

    


    
        




