# coding: utf-8
from sqlalchemy.sql.expression import func

from models.users import Users, UsersExtras
from models.extras import Extras
from utils.common import detetime_to_unixtime
from utils.exceptions import RequestErrorException
from utils.validation import validate_mLimit


def get(user_id, session, **kwargs):
    user = session.query(Users).get(user_id)
    if not user:
        raise RequestErrorException
    query = session.query(Extras).join(UsersExtras).filter(UsersExtras.user_id == user_id)

    if 'id' in kwargs['query']:
        if isinstance(kwargs['query']['id'], int):
            id_ = [kwargs['query']['id']]
        else:
            id_ = kwargs['query']['id']
        query = query.filter(Extras.id.in_(id_))

    if 'type' in kwargs['query']:
        query = query.filter(Extras.type == kwargs['query']['type'])

    if 'text' in kwargs['query']:
        query = query.filter(func.to_tsvector(Extras.description).match(kwargs['query']['text']))

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

    ret_list = []
    for extra in query.all():
        ret_list.append({
            'id': extra.id,
            'type': extra.type.code,
            'title': extra.title,
            'title_orig': extra.title_orig,
            'description': extra.description,
            'location': extra.location,
            'created': detetime_to_unixtime(extra.created),
        })

    return ret_list
