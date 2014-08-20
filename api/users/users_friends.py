# coding: utf-8
from models.users import Users, UsersRels
from models.tokens import SessionToken
from models.users.constants import APP_USERSRELS_TYPE_FRIEND
from utils.validation import validate_mLimit
from api.serializers import mUserShort


def get(user_id, auth_user, session, query, **kwargs):
    subquery = session.query(UsersRels.partner_id).filter_by(user_id=user_id, urStatus=APP_USERSRELS_TYPE_FRIEND).subquery()
    query = session.query(Users).filter(Users.id.in_(subquery))

    if 'is_online' in query:
        query = SessionToken.filter_users_is_online(query['is_online'], query)

    if 'text' in query:
        query = Users.full_text_search_by_last_first_name(query['text'], session, query)

    if 'is_person' in query:
        query = Users.filter_users_person(query['is_person'], session, query)

    if 'limit' in query:
        limit = validate_mLimit(query['limit'])

        # Set limit and offset filter
        if not limit is None:
            # Set Limit
            if limit[0]:
                query = query.limit(limit[0])

            # Set Offset
            if not limit[0] is None:
                query = query.offset(limit[1])

    return mUserShort(instance=query.all(), session=session, user=auth_user).data


