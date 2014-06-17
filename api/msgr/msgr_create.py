from requests import Response
from api.users.serializer import mUserShort
from models import db, MsgrThreads, UsersMsgrThreads, MsgrLog, Users
from utils import need_authorization


@db
@need_authorization
def put(user, session=None, **kwargs):
    if ('attachments' in kwargs or 'text' in kwargs):
        return ''
    users = session.query.filter(Users.id.in_(kwargs['user_ids']))
    user_msgr_threads = session.query(UsersMsgrThreads).filter_by(msgr_threads_id=kwargs['user_ids']).first()
    msgr_thread = session.query(MsgrThreads).filter_by(id=user_msgr_threads.msgr_threads_id).first()
    ml = MsgrLog(msgr_threads_id=msgr_thread.id, user_id=user_msgr_threads.user_id, text=kwargs['text'])
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