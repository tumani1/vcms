# coding: utf-8

from models import dbWrap, Topics
from models.topics.constants import TOPIC_TYPE

__all__ = ['get_topic_extars']


@dbWrap
def get_topic_extars(user, session, **kwargs):
    return {}

