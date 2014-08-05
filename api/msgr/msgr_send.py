# coding: utf-8

import datetime
from models.msgr import MsgrLog, UsersMsgrThreads, MsgrThreads
from utils import need_authorization


@need_authorization
def put(id, auth_user, session, **kwargs):
    msgr_thread = MsgrThreads.get_msgr_threads_by_id(session, id).first()

    if msgr_thread is None:
        return {'code': 400}

    query = kwargs['query']
    if 'text' in query:
        msgr_log = MsgrLog(msgr_threads_id=id, user_id=auth_user.id, text=query['text'])
    else:
        if 'attach' in query:
            msgr_log = MsgrLog(msgr_threads_id=id, user_id=auth_user.id, attachments=query['attach'])
        else:
            return {'code': 400}

    session.add(msgr_log)
    date = datetime.datetime.now()
    user_msgr_thread = UsersMsgrThreads.get_users_msgr_threads_by_msgr_thread_id(session, id).all()

    for user_msgr in user_msgr_thread:
        user_msgr.last_msg_sent = date
        user_msgr.last_visit = date

        if user_msgr.user_id != auth_user.id:
            user_msgr.new_msgs += 1
        session.add(user_msgr)

    session.commit()
