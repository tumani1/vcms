# coding: utf-8

from models.tokens import GlobalToken


def revoke(auth_user, session, query, **kwargs):
    '''
    Revoking access for users Global Token by deleting it
    '''
    if 'token' in query:
        gt = session.query(GlobalToken).filter(token=query['token']).first()
        session.delete(gt)
        session.commit()
