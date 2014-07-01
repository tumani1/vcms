from models import MsgrThreads, MsgrLog
from utils import need_authorization


@need_authorization
def get(auth_user, session, id, **kwargs):
    result = {
        'id': '',
        'text': '',
        'user': '',
        'created': '',
        'attach': '',
        'thread': ''
    }
    msgr_log = MsgrLog.get_msgr_log_by_msgr_thread_id(session, id)

