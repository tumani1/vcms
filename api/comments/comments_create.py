from models.comments.comments import Comments

def post():
    pass
def delete(auth_user, session, id, **kwargs):
    com  = Comments.get_comment_by_id(auth_user.id, session, id).first()
    session.delete(com)
    session.flush()
    session.commit()