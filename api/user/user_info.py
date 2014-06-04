from models import db, Users, Cities, Countries


@db
def get(user_id, session= None):
    user = session.query(Users).filter_by(id=user_id).first()
    city = session.query(Cities).filter_by(id=user.city_id).first()
    country = session.query(Countries).filter_by(id=city.country_id).first()
    result = {
        'id': user.id,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'userpic': user.firstname,
        'time_zone': user.time_zone,
        'country': country.name,
        'city': city.name,
    }
    return result
@db
def put(user_id, session=None,**kwargs):
    pass
