# coding: utf-8

from models import dbWrap, Topics

@dbWrap
def get_topics_list(user, name, session=None, **kwargs):
    instance = Topics.get_topics_by_name(user, name, session)

    return Topics.data(user, instance)
