# coding: utf-8

from models import Topics
from db_engine import db
from serializer import mTopicSerializer

__all__ = ['get_topic_info']


@db
def get_topic_info(auth_user, name, session, **kwargs):
    data = {}
    instance = Topics.get_topics_by_name(auth_user, name, session)

    if not instance is None:
        # Params
        params = {
            'user': auth_user,
            'instance': instance,
            'session': session,
        }

        data = mTopicSerializer(**params).data

    return data
