# coding: utf-8
from models import db
from models.users import Users, UsersRels
from models.users.constants import APP_USERSRELS_TYPE_UNDEF


@db
def get(user_id, id, session=None):
    user = session.query(Users).get(id)
    if not user:
        raise Exception()

    return_dict = dict(
        id=user.id,
        firstname=user.firstname,
        lastname=user.lastname,
        gender=user.gender.code,
        regdate=user.created,
        lastvisit=user.last_visit,
        is_online=False,
        city=user.city.name,
        country=user.city.country.name,
    )
    if user.person:
        return_dict['person_id'] = user.person.id

    if user_id:
        rel = session.query(UsersRels).filter_by(user_id=user_id, partner_id=id).first()
        if rel is None:
            status = APP_USERSRELS_TYPE_UNDEF
        else:
            status = rel.urStatus.code
        return_dict['relation'] = status

    return return_dict
