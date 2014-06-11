# coding: utf-8
from models import db
from models.users import Users, UsersRels
from models.users.constants import APP_USERSRELS_TYPE_UNDEF
from utils.exceptions import DoesNotExist


# TODO online
@db
def get(user, id, session=None, **kwargs):
    query = session.query(Users).get(id)
    if not query:
        raise DoesNotExist

    return_dict = dict(
        id=query.id,
        firstname=query.firstname,
        lastname=query.lastname,
        gender=query.gender.code,
        regdate=query.created,
        lastvisit=query.last_visit,
        is_online=False,
        city=query.city.name,
        country=query.city.country.name,
    )
    if query.person:
        return_dict['person_id'] = query.person.id

    if user:
        rel = session.query(UsersRels).filter_by(user_id=query, partner_id=id).first()
        if rel is None:
            status = APP_USERSRELS_TYPE_UNDEF
        else:
            status = rel.urStatus.code
        return_dict['relation'] = status

    return return_dict