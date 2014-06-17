import datetime
from requests import Response
from sqlalchemy import Date
from api.users.serializer import mUserShort
from models import db, MsgrThreads, UsersMsgrThreads, MsgrLog, Users
from utils import need_authorization


@db
@need_authorization
def put(user, session=None, **kwargs):
    # if ('attachments' in kwargs or 'text' in kwargs):
    #     return ''
    mt = MsgrThreads(msg_cnt=1)
    session.add(mt)
    session.commit()
    users = session.query(Users).filter(Users.id.in_(kwargs['user_ids']))
    for id in kwargs['user_ids']:
        user_msgr_threads = UsersMsgrThreads(user_id=id, msgr_threads_id=mt.id, new_msgs=1)
        session.add(user_msgr_threads)
    date = datetime.datetime.now()
    user_msgr_threads = UsersMsgrThreads(user_id=user.id, msgr_thread_id=mt.id, last_msg_sent=date, last_visit=date, new_msgs=0)
    session.add(user_msgr_threads)

    ml = MsgrLog(msgr_threads_id=mt.id, user_id=user.id, text=kwargs['text'])
    session.add(ml)
    params = {
        'user': user,
        'session': session,
        'instance': users
    }

    session.commit()
    m_user_short = mUserShort(**params).data
    result = {
        'id': "",
        'msgr_cnt': '',
        'users': m_user_short
    }
    return result