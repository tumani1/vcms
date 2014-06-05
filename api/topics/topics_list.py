# coding: utf-8

from models import dbWrap, Topics
from models.topics.constants import TOPIC_TYPE

@dbWrap
def get_topics_list(user, session=None, **kwargs):
    name = None
    if 'name' in kwargs:
        try:
            name = str(kwargs['name'])
        except Exception, e:
            pass

    text = None
    if 'text' in kwargs:
        try:
            text = str(kwargs['text'])
        except Exception, e:
            pass

    type = None
    if 'type' in kwargs:
        if kwargs['type'] in dict(TOPIC_TYPE).keys():
            type = kwargs['type']

    limit = None
    if 'limit' in kwargs:
        result = kwargs['limit'].split(',', 1)

        if len(result) == 1:
            limit = (result[0], 0)
        elif len(result) == 2:
            # Check limit
            if not len(result[0]):
                r1 = None
            else:
                try:
                    r1 = int(result[0])
                except Exception, e:
                    r1 = None

            # Check top
            try:
                r2 = int(result[1])
            except Exception, e:
                r2 = 0

            limit = (r1, r2)

    query = Topics.tmpl_for_topics(user, session)

    # Set name filter
    if not name is None:
        query = query.filter(Topics.name == name)

    # Set description filter
    # if not text is None:
    #     query = query.filter(Topics.description == text)

    # Set type filter
    if not type is None:
        query = query.filter(Topics.type == type)

    # Set limit and offset filter
    if not limit is None:
        # Set Limit
        if limit[0]:
            query = query.limit(limit[0])

        # Set Offset
        if not limit[0] is None:
            query = query.offset(limit[1])

    return Topics.data(user, query)
