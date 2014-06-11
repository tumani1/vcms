# coding: utf-8

from models import db, Persons
from api.persons.serializer import mPersonSerializer

from utils.validation import validate_int

__all__ = ['get_person_info']


@db
def get_person_info(user, person, session, **kwargs):
    # Validation person value
    person = validate_int(person, min_value=1)
    if type(person) == Exception:
        return {'code': 404}

    instance = Persons.get_persons_by_id(user, person, session).first()

    params = {
        'instance': instance,
        'user': user,
        'session': session,
    }

    return mPersonSerializer(**params).data
