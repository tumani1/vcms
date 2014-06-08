# coding: utf-8

from models import db, Persons
from api.persons.serializer import mPersonSerializer

__all__ = ['get_person_info']


@db
def get_person_info(user, person, session, **kwargs):
    instance = Persons.get_persons_by_id(user, person, session).first()

    return mPersonSerializer(instance, user).data
