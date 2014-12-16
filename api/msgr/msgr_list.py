# coding: utf-8

from models.msgr import UsersMsgrThreads, MsgrThreads
from api.msgr.msgr_info import get as get_msgr_info

from utils import need_authorization


@need_authorization
def get(auth_user, session=None, **kwargs):
    result = []
    query = kwargs['query_params']
    if 'user_author' in query:
        msgr_threads_ids = session.query(UsersMsgrThreads.msgr_threads_id).filter(UsersMsgrThreads.user_id.in_(query['user_author'])).distinct().all()
        msgr_threads_ids = [i[0] for i in msgr_threads_ids]
    else:
        msgr_threads_ids = session.query(MsgrThreads.id).all()
        msgr_threads_ids = [i[0] for i in msgr_threads_ids]

    for msgr_thread in msgr_threads_ids:
        m_msgr_thread = get_msgr_info(id=msgr_thread, auth_user=auth_user, session=session)
        result.append(m_msgr_thread)

    return result


