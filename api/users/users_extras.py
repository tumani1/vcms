# coding: utf-8
from sqlalchemy.sql.expression import func

from models import db
from models.users import Users, UsersExtras
from models.extras import Extras
from utils.exceptions import DoesNotExist
from utils.validation import validate_mLimit


@db
def get(user_id, session=None, type=None, limit=',0', text=None, id=None, **kwargs):
    user = session.query(Users).get(user_id)
    if not user:
        raise DoesNotExist
    query = session.query(Extras).join(UsersExtras).filter(UsersExtras.user_id == user_id)
    if not id is None:
        if isinstance(id, int):
            id = [id]
        query = query.filter(Extras.id.in_(id))
    if not type is None:
        query = query.filter(Extras.type == type)
    if not text is None:
        query = query.filter(func.to_tsvector(Extras.description).match(text))

    limit = validate_mLimit(limit)
     # Set limit and offset filter
    if not limit is None:
        # Set Limit
        if limit[0]:
            query = query.limit(limit[0])

        # Set Offset
        if not limit[0] is None:
            query = query.offset(limit[1])

    ret_list = []
    for extra in query:
        ret_list.append({
            'id': extra.id,
            'type': extra.type,
            'title': extra.title,
            'title_orig': extra.title_orig,
            'description': extra.description,
            'location': extra.location,
            'created': extra.created,
        })

    return ret_list