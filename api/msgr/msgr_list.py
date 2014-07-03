
from api.users.serializer import mUserShort
from models import UsersMsgrThreads, Users
from utils import need_authorization


@need_authorization
def get(user, session=None, **kwargs):
    result = []
    params = {
        'user': user,
        'session': session,
        'instance': ''
        }

    if 'user_author' in kwargs:
        params['instance'] = Users.get_users_by_id(session, kwargs['user_author']).all()
        msgr_threads = UsersMsgrThreads.join_with_msgr_threads(user, session, user_author=kwargs['user_author']).all()
    else:
        msgr_threads = UsersMsgrThreads.join_with_msgr_threads(user, session).all()
        params['instance'] = user

    for user_msgr_thread in msgr_threads:
        if not user_msgr_thread.msgr_threads is None:
            m_msgr_thread = {
                'id': user_msgr_thread.msgr_threads.id,
                'msgr_cnt': user_msgr_thread.msgr_threads.msg_cnt,
                'users': mUserShort(**params).data

            }
            result.append(m_msgr_thread)
    return result


