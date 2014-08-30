# coding: utf-8

from models.users import Users
from models.msgr import UsersMsgrThreads

from api.serializers import mUserShort

from utils import need_authorization


@need_authorization
def get(auth_user, session=None, **kwargs):
    result = []
    params = {
        'user': auth_user,
        'session': session,
        'instance': ''
        }

    query = kwargs['query_params']
    if 'user_author' in query:
        params['instance'] = Users.get_users_by_id(session, query['user_author']).all()
        msgr_threads = UsersMsgrThreads.join_with_msgr_threads(auth_user, session, user_author=query['user_author']).all()
    else:
        msgr_threads = UsersMsgrThreads.join_with_msgr_threads(auth_user, session).all()
        params['instance'] = auth_user

    for user_msgr_thread in msgr_threads:
        if not user_msgr_thread.msgr_threads is None:
            m_msgr_thread = {
                'id': user_msgr_thread.msgr_threads.id,
                'msgr_cnt': user_msgr_thread.msgr_threads.msg_cnt,
                'users': mUserShort(**params).data

            }
            result.append(m_msgr_thread)

    return result


