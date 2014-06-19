# coding: utf-8

from models import Persons
from db_engine import db
from api.persons.serializer import mPersonSerializer

from utils.validation import validate_int

__all__ = ['get_person_info']


@db
def get_person_info(auth_user, person, session, **kwargs):
    # Validation person value
    person = validate_int(person, min_value=1)
    if type(person) == Exception:
        return {'code': 404}

    data = {}
    instance = Persons.get_persons_by_id(auth_user, person, session).first()

    if not instance is None:
        params = {
            'instance': [instance],
            'user': auth_user,
            'session': session,
        }

        data = mPersonSerializer(**params).data

    return data
