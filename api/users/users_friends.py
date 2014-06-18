# coding: utf-8
from models import db
from models.users import Users, UsersRels
from models.tokens import SessionToken
from models.users.constants import APP_USERSRELS_TYPE_FRIEND
from utils.validation import validate_mLimit
from serializer import mUserShort
from settings import TOKEN_LIFETIME

from datetime import datetime, timedelta


@db
def get(user, id, session=None, type=None, limit=',0', text=None, is_online=None,
        is_person=None, **kwargs):
    subquery = session.query(UsersRels.partner_id).filter_by(user_id=id, urStatus=APP_USERSRELS_TYPE_FRIEND).subquery()
    query = session.query(Users).filter(Users.id.in_(subquery))

    if not is_online is None:
        query = query.join(SessionToken).filter(SessionToken.is_active, SessionToken.created - datetime.utcnow() < timedelta(minutes=TOKEN_LIFETIME))

    if not text is None:
        query = Users.full_text_search_by_last_first_name(text, session, query)

    if not is_person is None:
        query = Users.filter_users_person(is_person, session, query)

    limit = validate_mLimit(limit)
     # Set limit and offset filter
    if not limit is None:
        # Set Limit
        if limit[0]:
            query = query.limit(limit[0])

        # Set Offset
        if not limit[0] is None:
            query = query.offset(limit[1])

    return mUserShort(instance=query.all(), session=session, user=user).data