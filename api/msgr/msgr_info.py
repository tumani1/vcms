from api.users.serializer import mUserShort
from models import UsersMsgrThreads, MsgrThreads
from utils import need_authorization


@need_authorization
def get(user, session, id):
    users_msgr_threads = UsersMsgrThreads.get_users_msgr_threads_by_msgr_thread_id(session, id).first()
    params = {
        'user': user,
        'session': session,
        'instance': users_msgr_threads
    }
    m_user_short = mUserShort(**params).data
    msgr_threads = MsgrThreads.get_msgr_threads_by_id(session, id).first()

    result = {
        'id': msgr_threads.id,
        'msgr_cnt': msgr_threads.msg_cnt,
        'users': m_user_short
    }
    return result

