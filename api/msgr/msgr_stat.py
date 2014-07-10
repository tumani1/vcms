# coding: utf-8
from utils import need_authorization
from models.msgr import UsersMsgrThreads


@need_authorization
def get(auth_user, session=None):
    users_msgr_threads = session.query(UsersMsgrThreads).filter(UsersMsgrThreads.user_id==auth_user.id).first()
    result = {
        'new_msgs': users_msgr_threads.new_msgs,
    }
    return result
