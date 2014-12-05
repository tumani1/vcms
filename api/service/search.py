# coding: utf-8

from models.persons import Persons
from models.topics.constants import TOPIC_TYPE

from utils.validation import validate_list_int, validate_mLimit, validate_string
from api.serializers import mPersonSerializer, mPersonRoleSerializer

__all__ = ['get_search_list']


def get_search_list(auth_user, session, **kwargs):
    pass
