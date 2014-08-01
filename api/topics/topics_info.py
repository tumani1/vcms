# coding: utf-8

from models.topics import Topics
from api.serializers import mTopicSerializer

__all__ = ['get_topic_info']


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
