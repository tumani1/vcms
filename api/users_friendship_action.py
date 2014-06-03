# coding: utf-8
from sqlalchemy.orm import sessionmaker

from models import engine, UsersRels


def get(user_id, partner_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(UsersRels.urStatus).filter_by(user_id=user_id, partner_id=partner_id)
