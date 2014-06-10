# coding: utf-8
from models import db
from models.users import Users, UsersRels
from models.users.constants import APP_USERSRELS_TYPE_FRIEND
from utils.validation import validate_mLimit


# TODO: online person type text
@db
def get(user, id, session=None, type=None, limit=',0', text='', is_online=None,
        is_person=None, **kwargs):
    subquery = session.query(UsersRels.partner_id).filter_by(user_id=id).subquery()
    query = session.query(Users).filter(Users.id.in_(subquery))

    if type:
        pass
    if is_person:
        pass
    if is_online:
        pass

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
    for u in query:
        ret_dict = dict(
            id=u.id,
            firtsname=u.firtsname,
            lastname=u.lastname,
            is_online=False,
            person_id=None,
        )
        if user:
            ret_dict['relation'] = APP_USERSRELS_TYPE_FRIEND
        ret_list.append(ret_dict)

    return ret_list