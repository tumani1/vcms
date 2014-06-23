import datetime
from api.users.serializer import mUserShort
from models import db, MsgrThreads, UsersMsgrThreads, MsgrLog, Users
from utils import need_authorization


@db
@need_authorization
def put(user, session=None, **kwargs):
    mt = MsgrThreads(msg_cnt=1)
    session.add(mt)
    session.commit()
    users = Users.get_users_by_id(session, kwargs['user_ids']).all()
    for id in kwargs['user_ids']:
        user_msgr_threads = UsersMsgrThreads(user_id=id, msgr_threads_id=mt.id, new_msgs=1)
        session.add(user_msgr_threads)
    date = datetime.datetime.now()
    user_msgr_threads = UsersMsgrThreads(user_id=user.id, msgr_threads_id=mt.id, last_msg_sent=date, last_visit=date, new_msgs=0)
    session.add(user_msgr_threads)
    if 'attachments' in kwargs:
        ml = MsgrLog(msgr_threads_id=mt.id, user_id=user.id, attachments=kwargs['attachments'])
    else:
        if 'text' in kwargs:
            ml = MsgrLog(msgr_threads_id=mt.id, user_id=user.id, text=kwargs['text'])
        else:
            return {'code': 400}
    session.add(ml)
    params = {
        'user': user,
        'session': session,
        'instance': users
    }

    # m_user_short = mUserShort(**params).data
    session.commit()
    result = {
        'id': mt.id,
        'msgr_cnt': mt.msg_cnt,
        'users': ''
    }
    return result

