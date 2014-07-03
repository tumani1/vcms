# coding: utf-8
from utils import need_authorization
from models.msgr import UsersMsgrThreads


@need_authorization
def get(user, session=None):
    users_msgr_threads = session.query(UsersMsgrThreads).filter(UsersMsgrThreads.user_id==user.id).first()
    result = {
        'new_msgs': users_msgr_threads.new_msgs,
    }
    return result