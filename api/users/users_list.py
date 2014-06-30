# coding: utf-8
from models.users import Users, UsersRels
from models.tokens import SessionToken
from utils.validation import validate_mLimit
from serializer import mUser


def get(auth_user, session, id=None, is_online=None, is_person=None, text=None,
        city=None, limit=',0', country=None, friendship=None, **kwargs):
    query = Users.tmpl_for_users(session)

    if id:
        if isinstance(id, int):
            id = [id]
        query = query.filter(Users.id.in_(id))

    if not text is None:
        query = Users.full_text_search_by_last_first_name(query=query, session=session, text=text)

    if not friendship is None:
        query = UsersRels.filter_users_by_status(friendship, query)

    if not is_online is None:
        query = SessionToken.filter_users_is_online(is_online, query)

    if not is_person is None:
        query = Users.filter_users_person(is_person=is_person, session=session, query=query)

    if not city is None:
        query = Users.filter_by_cities(city, session, query)

    if not country is None:
        query = Users.filter_by_country(country, session, query)

    limit = validate_mLimit(limit)
     # Set limit and offset filter
    if not limit is None:
        # Set Limit
        if limit[0]:
            query = query.limit(limit[0])

        # Set Offset
        if not limit[0] is None:
            query = query.offset(limit[1])

    return mUser(user=auth_user, instance=query.all(), session=session).data
