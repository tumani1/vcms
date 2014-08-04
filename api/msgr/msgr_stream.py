# coding: utf-8

from api.serializers import mUserShort

from models.msgr import MsgrLog
from models.users import Users

from utils import need_authorization
from utils.validation import validate_mLimitId


@need_authorization
def get(auth_user, session, id, **kwargs):
    result = []
    params = {
        'user': auth_user,
        'session': session,
        'instance': ''
    }
    if 'limit' in kwargs:
        limit = validate_mLimitId(kwargs['limit'])
        msgr_log = MsgrLog.get_msgr_log_by_msgr_thread_id_limit(session, id, limit).all()
    else:
        msgr_log = MsgrLog.get_msgr_log_by_msgr_thread_id(session, id).all()
    for msg in msgr_log:
        user = Users.get_users_by_id(session, [msg.user_id]).first()
        params['instance'] = user
        mMsgrMsg = {
            'id': msg.id,
            'text': msg.text,
            'user': mUserShort(**params).data,
            'created': msg.created.strftime('%Y-%m-%d'),
            'attach': msg.attachments,
            'thread': msg.msgr_threads_id
        }
        result.append(mMsgrMsg)
    return result
