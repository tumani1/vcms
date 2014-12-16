# coding: utf-8

from api.serializers import mUserShort
from models import Users
from models.msgr import UsersMsgrThreads, MsgrThreads
from utils import need_authorization


@need_authorization
def get(id, auth_user, session, **kwargs):
    users_ids_msgr_threads = session.query(UsersMsgrThreads.user_id).filter(UsersMsgrThreads.msgr_threads_id == id).all()#UsersMsgrThreads.get_users_msgr_threads_by_msgr_thread_id(session, id).all()
    users_ids_msgr_threads = [i[0] for i in users_ids_msgr_threads]
    users_in_thread = Users.get_users_by_id(session, users_ids_msgr_threads).all()
    params = {
        'user': auth_user,
        'session': session,
        'instance': users_in_thread
    }
    m_user_short = mUserShort(**params).data
    msgr_threads = MsgrThreads.get_msgr_threads_by_id(session, id).first()

    result = {
        'id': msgr_threads.id,
        'msgr_cnt': msgr_threads.msg_cnt,
        'users': m_user_short
    }
    return result

