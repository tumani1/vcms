# coding: utf-8

from models.persons import Persons
from api.serializers import mPersonSerializer

from utils.validation import validate_int

__all__ = ['get_person_info']


def get_person_info(person_id, auth_user, session, **kwargs):
    # Validation person value
    person_id = validate_int(person_id, min_value=1)

    data = {}
    instance = Persons.get_persons_by_id(auth_user, person_id, session).first()

    if not instance is None:
        params = {
            'instance': instance,
            'user': auth_user,
            'session': session,
        }

        data = mPersonSerializer(**params).data

    return data
