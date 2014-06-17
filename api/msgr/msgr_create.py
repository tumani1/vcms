from requests import Response
from models import db, MsgrThreads, UsersMsgrThreads, MsgrLog
from utils import need_authorization


@db
@need_authorization
def put(user, session=None, **kwargs):
    if ('attachments' in kwargs or 'text' in kwargs):
        return Response.status_code
    user_msgr_threads = session.query(UsersMsgrThreads).filter_by(msgr_threads_id=kwargs['user_ids']).first()
    msgr_thread = session.query(MsgrThreads).filter_by(id=user_msgr_threads.msgr_threads_id).first()
    ml = MsgrLog(msgr_threads_id=msgr_thread.id, user_id=user_msgr_threads.user_id, text=kwargs['text'])
    session.add(ml)
    session.commit()
