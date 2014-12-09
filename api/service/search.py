# coding: utf-8

import json
from Queue import Queue
from threading import Thread

from models import Persons, Topics, Media, MediaUnits, Content
from utils.constants import OBJECT_TYPE_PERSON, OBJECT_TYPE_TOPIC, OBJECT_TYPE_MEDIA_UNIT, OBJECT_TYPE_MEDIA

from utils.exceptions import RequestErrorException
from utils.validation import validate_mLimit, validate_string

__all__ = ['get_search_list']


def convert_result_search(type_obj, obj):
    return {'type': type_obj, 'obj': obj.as_dict}


def gq(model, *args, **kwargs):
    return model.get_search_by_text(**kwargs)


def get_search_list(auth_user, session, **kwargs):
    # Params
    params = {
        'limit': None,
        'text': None,
        'session': session,
        'list_ids': [],
    }

    query = kwargs['query_params']

    if 'text' in query:
        params['text'] = validate_string(query['text'])

    if 'limit' in query:
        # limit = query.get('limit', '')
        # limit, top = validate_mLimit(limit)
        params['limit'] = 10

    text = params['text']
    if text is None:
        raise RequestErrorException(u'Empty text field')

    mds = {
        Persons: (OBJECT_TYPE_PERSON, 'person',),
        Topics: (OBJECT_TYPE_TOPIC, 'topic',),
        Media: (OBJECT_TYPE_MEDIA, 'media',),
        MediaUnits: (OBJECT_TYPE_MEDIA_UNIT, 'mediaunit',),
    }

    result = []
    append = result.append

    content_ids = {}
    con = Content.get_search_by_text(**params)
    for i in con:
        if not i.obj_type.code in content_ids:
            content_ids[i.obj_type.code] = []

        content_ids[i.obj_type.code].append(i.obj_id)

    # workers = []
    # queue = Queue()
    #
    # for md in mds.keys():
    #     list_ids = content_ids.get(mds[Persons], [])
    #     if len(list_ids):
    #         params.update({'list_ids': list_ids})
    #         workers.append(Thread(target=lambda q, arg, kw: q.put(gq(*arg, **kw)), args=(queue, md,), kwargs=params))
    #         workers[-1].start()
    #
    # for w in workers:
    #     w.join()
    #
    # while not queue.empty():
    #     print "Result: %s" % queue.get()
    #     append(convert_result_search(queue.get()))

    for key, val in mds:
        list_ids = content_ids.get(val[0], [])
        if len(list_ids):
            params.update({'list_ids': list_ids})
            obj_search = key.get_search_by_text(**params)

            for item in obj_search:
                append(convert_result_search(val[1], item))

    return result
