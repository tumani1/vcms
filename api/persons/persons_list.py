# coding: utf-8

from models import db, Persons

__all__ = ['get_person_list']


@db
def get_person_list(user, session, **kwargs):
    pass
