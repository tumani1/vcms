# coding: utf-8

import datetime

from models.msgr import MsgrThreads, UsersMsgrThreads, MsgrLog
from models.users import Users

from api.serializers import mUserShort
from utils import need_authorization


@need_authorization
def put(auth_user, session=None, **kwargs):
    mt = MsgrThreads(msg_cnt=1)
    session.add(mt)
    session.commit()

    query = kwargs['query_params']
    users = Users.get_users_by_id(session, query['user_ids']).all()
    for id in query['user_ids']:
        if id != auth_user.id:
            session.add(UsersMsgrThreads(user_id=id, msgr_threads_id=mt.id, new_msgs=1))

    date = datetime.datetime.now()
    user_msgr_threads = UsersMsgrThreads(user_id=auth_user.id, msgr_threads_id=mt.id, last_msg_sent=date, last_visit=date, new_msgs=0)
    session.add(user_msgr_threads)

    if 'attachments' in query:
        ml = MsgrLog(msgr_threads_id=mt.id, user_id=auth_user.id, attachments=query['attachments'])
    else:
        if 'text' in query:
            ml = MsgrLog(msgr_threads_id=mt.id, user_id=auth_user.id, text=query['text'])
        else:
            return {'code': 400}
    session.add(ml)

    params = {
        'user': auth_user,
        'session': session,
        'instance': users
    }

    m_user_short = mUserShort(**params).data
    session.commit()

    result = {
        'id': mt.id,
        'msgr_cnt': mt.msg_cnt,
        'users': m_user_short
    }
    return result

