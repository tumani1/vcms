# coding: utf-8

from models import dbWrap, Topics

__all__ = ['get_topic_info']


@dbWrap
def get_topic_info(user, name, session, **kwargs):
    instance = Topics.get_topics_by_name(user, name, session)

    return Topics.data(user, instance)
