# coding: utf-8
from models import db
from models.users import UsersRels, Users
from models.contents import Cities, Countries
from models.users.constants import APP_USERSRELS_TYPE_UNDEF
from utils.validation import validate_mLimit


# TODO person and online and text
@db
def get(user, session=None, id=None, is_online=None, is_person=None, text='',
        city=None, limit=',0', country=None, **kwargs):
    query = session.query(Users)

    if id:
        if isinstance(id, int):
            id = [id]
        query = query.filter(Users.id.in_(id))

    if text:
        pass
    if is_online:
        pass
    if is_person:
        pass

    if city:
        query = query.join(Cities).filter(Cities.name == city.encode('utf-8'))

    if country:
        query = query.join(Cities).join(Countries).filter(Countries.name == city.encode('utf-8'))

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
            firstname=u.firstname,
            lastname=u.lastname,
            gender=u.gender.code,
            regdate=u.created,
            lastvisit=u.last_visit,
            is_online=is_online or False,
            city=u.city.name,
            country=u.city.country.name,

        )
        if u.person and is_person:
            ret_dict['person_id'] = u.person.id
        if user:
         ret_dict['relation'] = session.query(UsersRels.urStatus).filter_by(user_id=user, partner_id=u.id).first()

        ret_list.append(ret_dict)

    return ret_list