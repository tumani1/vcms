# coding: utf-8
from models import GlobalToken


def revoke(auth_user, x_token, token, session):
    '''
    Revoking access for users Global Token by deleting it
    '''

    gt = session.query(GlobalToken).filter(token = token).first()

    session.delete(gt)
    session.commit()

    