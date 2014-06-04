# coding: utf-8

from models import dbWrap, Topics

@dbWrap
def get_topics_info(user, name, session=None, **kwargs):
    instance = Topics.get_topics_by_name(user, name, session)
    instance = [i for i in instance]
    print instance
    print "Instance: %s" % instance

    return instance
