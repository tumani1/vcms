from models import db, Users


@db
def put(user_id, password, session=None):
    user = session.query(Users).filter_by(id=user_id).first()
    user.password = password
    session.commit()



