# coding: utf-8
from models.users import Users, UsersRels
from models.tokens import SessionToken
from utils.validation import validate_mLimit
from api.serializers import mUser


def get(auth_user, session, **kwargs):
    query = Users.tmpl_for_users(session)

    if 'id' in kwargs['query']:
        if isinstance(kwargs['query']['id'], int):
            id_ = [kwargs['query']['id']]
        else:
            id_ = kwargs['query']['id']
        query = query.filter(Users.id.in_(id_))

    if 'text' in kwargs['query']:
        query = Users.full_text_search_by_last_first_name(query=query, session=session, text=kwargs['query']['text'])

    if 'friendship' in kwargs['query']:
        query = UsersRels.filter_users_by_status(kwargs['query']['friendship'], query)

    if 'is_online' in kwargs['query']:
        query = SessionToken.filter_users_is_online(kwargs['query']['is_online'], query)

    if 'is_person' in kwargs['query']:
        query = Users.filter_users_person(is_person=kwargs['query']['is_person'], session=session, query=query)

    if 'city' in kwargs['query']:
        query = Users.filter_by_cities(kwargs['query']['city'], session, query)

    if 'country' in kwargs['query']:
        query = Users.filter_by_country(kwargs['query']['country'], session, query)

    if 'limit' in kwargs['query']:
        limit = validate_mLimit(kwargs['query']['limit'])
         # Set limit and offset filter
        if not limit is None:
            # Set Limit
            if limit[0]:
                query = query.limit(limit[0])

            # Set Offset
            if not limit[0] is None:
                query = query.offset(limit[1])

    return mUser(user=auth_user, instance=query.all(), session=session).data
