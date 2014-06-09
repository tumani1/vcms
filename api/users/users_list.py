# coding: utf-8
from models import db
from models.users import UsersRels, Users
from models.contents import Cities, Countries
from models.users.constants import APP_USERSRELS_TYPE_UNDEF
from utils.validation import validate_mLimit


# TODO person and online and text
@db
def get(user, session=None, **kwargs):
    query = session.query(Users)

    ids = kwargs.get('id', [])
    if ids:
        if isinstance(ids, int):
            ids = [ids]
        query = query.filter(Users.id.in_(ids))

    text = kwargs.get('text', '')
    if text:
        pass

    is_online = kwargs.get('is_online', None)
    is_person = kwargs.get('is_person', None)

    city = kwargs.get('city', None)
    if city:
        query = query.join(Cities).filter(Cities.name == city.encode('utf-8'))

    country = kwargs.get('country', None)
    if country:
        query = query.join(Cities).join(Countries).filter(Countries.name == city.encode('utf-8'))

    limit = validate_mLimit(kwargs.get('limit', ',0'))
     # Set limit and offset filter
    if not limit is None:
        # Set Limit
        if limit[0]:
            query = query.limit(limit[0])

        # Set Offset
        if not limit[0] is None:
            query = query.offset(limit[1])

    ret_list = []
    for user in query:
        status = APP_USERSRELS_TYPE_UNDEF
        ret_list.append(dict(
            id=user.id,
            firstname=user.firstname,
            lastname=user.lastname,
            gender=user.gender.code,
            regdate=user.created,
            lastvisit=user.last_visit,
            is_online=is_online or False,
            person_id=0,
            city=user.city.name,
            country=user.city.country.name,
            relation=status,
        ))

    return ret_list

get(None, id=1, city=u'Ярославль')