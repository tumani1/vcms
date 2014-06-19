from db_engine import db
from models import MsgrThreads, MsgrLog
from utils import need_authorization


@need_authorization
@db
def get(auth_user, id, session, **kwargs):
    msgr_thread = MsgrThreads.get_msgr_threads_by_id(session, id).first()
    msgr_log = MsgrLog.msgr_threads_id(session, id).first()

