# coding: utf-8
from sqlalchemy.sql.expression import func

from models.users import Users, UsersExtras
from models.extras import Extras
from utils.common import datetime_to_unixtime
from utils.exceptions import RequestErrorException
from utils.validation import validate_mLimit


def get(user_id, session, query, **kwargs):
    user = session.query(Users).get(user_id)
    if not user:
        raise RequestErrorException
    query = session.query(Extras).join(UsersExtras).filter(UsersExtras.user_id == user_id)

    if 'id' in query:
        if isinstance(query['id'], int):
            id_ = [query['id']]
        else:
            id_ = query['id']
        query = query.filter(Extras.id.in_(id_))

    if 'type' in query:
        query = query.filter(Extras.type == query['type'])

    if 'text' in query:
        query = query.filter(func.to_tsvector(Extras.description).match(query['text']))

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

    ret_list = []
    for extra in query.all():
        ret_list.append({
            'id': extra.id,
            'type': extra.type.code,
            'title': extra.title,
            'title_orig': extra.title_orig,
            'description': extra.description,
            'location': extra.location,
            'created': datetime_to_unixtime(extra.created),
        })

    return ret_list
