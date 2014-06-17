from models import GlobalToken

def revoke(user,x_token,token,session = None):
    '''
    Revoking access for users Global Token by deleting it
    '''

    gt = session.query(GlobalToken).filter(token = token).first()

    session.delete(gt)
    session.commit()

    