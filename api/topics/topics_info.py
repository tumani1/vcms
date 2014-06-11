# coding: utf-8

from models import db, Topics
from serializer import mTopicSerializer

__all__ = ['get_topic_info']


@db
def get_topic_info(user, name, session, **kwargs):
    instance = Topics.get_topics_by_name(user, name, session)

    # Params
    params = {
        'user': user,
        'instance': instance,
        'session': session,
    }

    return mTopicSerializer(**params).data
