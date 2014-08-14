# coding: utf-8
from models.users import Users, UsersRels
from models.tokens import SessionToken
from utils.validation import validate_mLimit
from api.serializers import mUser


def get(auth_user, session, query, **kwargs):
    query = Users.tmpl_for_users(session)

    if 'id' in query:
        if isinstance(query['id'], int):
            id_ = [query['id']]
        else:
            id_ = query['id']
        query = query.filter(Users.id.in_(id_))

    if 'text' in query:
        query = Users.full_text_search_by_last_first_name(query=query, session=session, text=query['text'])

    if 'friendship' in query:
        query = UsersRels.filter_users_by_status(query['friendship'], query)

    if 'is_online' in query:
        query = SessionToken.filter_users_is_online(query['is_online'], query)

    if 'is_person' in query:
        query = Users.filter_users_person(is_person=query['is_person'], session=session, query=query)

    if 'city' in query:
        query = Users.filter_by_cities(query['city'], session, query)

    if 'country' in query:
        query = Users.filter_by_country(query['country'], session, query)

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

    return mUser(user=auth_user, instance=query.all(), session=session).data
