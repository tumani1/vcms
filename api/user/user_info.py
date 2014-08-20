# coding: utf-8

from models.users import Users
from models.locations import Cities, Countries
from utils import need_authorization


@need_authorization
def get(auth_user, session=None, **kwargs):
    user = session.query(Users).filter_by(id=auth_user.id).first()
    city = session.query(Cities).filter_by(id=user.city_id).first()
    country = session.query(Countries).filter_by(id=city.country_id).first()
    result = {
        'id': user.id,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'userpic': user.firstname,
        'time_zone': str(user.time_zone),
        'country': country.name,
        'city': city.name,
    }
    return result



@need_authorization
def put(auth_user, session, **kwargs):
    query = kwargs['query']
    user = session.query(Users).filter_by(id=auth_user.id).first()

    if 'firstname' in query:
        user.firstname = query['firstname']

    if 'lastname' in query:
        user.lastname = query['lastname']

    if 'time_zone' in query:
        user.time_zone = query['time_zone']

    if session.dirty:
        session.commit()

