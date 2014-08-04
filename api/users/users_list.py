# coding: utf-8
from models.users import Users, UsersRels
from models.tokens import SessionToken
from utils.validation import validate_mLimit
from api.serializers import mUser


def get(auth_user, session, **kwargs):
    query = Users.tmpl_for_users(session)

    if 'id' in kwargs:
        if isinstance(kwargs['id'], int):
            id_ = [kwargs['id']]
        else:
            id_ = kwargs['id']
        query = query.filter(Users.id.in_(id_))

    if 'text' in kwargs:
        query = Users.full_text_search_by_last_first_name(query=query, session=session, text=kwargs['text'])

    if 'friendship' in kwargs:
        query = UsersRels.filter_users_by_status(kwargs['friendship'], query)

    if 'is_online' in kwargs:
        query = SessionToken.filter_users_is_online(kwargs['is_online'], query)

    if 'is_person' in kwargs:
        query = Users.filter_users_person(is_person=kwargs['is_person'], session=session, query=query)

    if 'city' in kwargs:
        query = Users.filter_by_cities(kwargs['city'], session, query)

    if 'country' in kwargs:
        query = Users.filter_by_country(kwargs['country'], session, query)

    if 'limit' in kwargs:
        limit = validate_mLimit(kwargs['limit'])
         # Set limit and offset filter
        if not limit is None:
            # Set Limit
            if limit[0]:
                query = query.limit(limit[0])

            # Set Offset
            if not limit[0] is None:
                query = query.offset(limit[1])

    return mUser(user=auth_user, instance=query.all(), session=session).data
