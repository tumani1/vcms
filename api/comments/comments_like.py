# coding: utf-8
import datetime
from models.comments.comments import Comments
from models.comments.users_comments import UsersComments
from utils.validation import validate_int


def put(auth_user, session, id, **kwargs):
    comment_id = validate_int(id)
    u_comment = UsersComments.get_user_comments(auth_user.id, session, comment_id)
    date = datetime.datetime.utcnow()
    if u_comment is None:
        u_comment = UsersComments(user_id=auth_user.id, comment_id=comment_id, liked=date)
        session.add(u_comment)
    elif u_comment.liked is None:
        u_comment.liked = date
    if session.new or session.dirty:
        session.commit()


def delete(auth_user, session, id, **kwargs):
    comment_id = validate_int(id)
    u_comment = UsersComments.get_user_comments(auth_user.id, session, comment_id)
    if not u_comment is None:
        u_comment.liked = None
    if session.dirty:
        session.commit()
