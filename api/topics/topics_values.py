# coding: utf-8

from models import dbWrap, TopicsValues

__all__ = ['get_topic_values']


@dbWrap
def get_topic_values(user, session, **kwargs):
    # Params
    params = {
        'user': user,
        'session': session,
        'name': None,
    }

    if 'name' in kwargs:
        name = kwargs['name']
        if not isinstance(name, list):
            try:
                params['name'] = str(name).strip()
            except Exception, e:
                pass
        else:
            if isinstance(name, list):
                try:
                    params['name'] = [str(i).strip() for i in name]
                except Exception, e:
                    pass

    if params['name'] is None:
        #return 404
        pass

    query = TopicsValues.tmpl_for_values(session).filter(TopicsValues.name.in_(name))

    return TopicsValues.data(query)
