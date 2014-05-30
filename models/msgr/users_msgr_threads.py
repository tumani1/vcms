# coding: utf-8
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy_utils import ChoiceType

from models import Base


class UsersMsgrThreads(Base):
    __tablename__ = 'users_msgr_threads'
    __table_args__ = {'extend_existing': True}

    TYPE_STATUS = (
        (0, u'Заблокирован'),
        (1, u'Не заблокирован'),
    )

    user_id         = Column(Integer, ForeignKey("users.id"), primary_key=True)
    msgr_threads_id = Column(Integer, ForeignKey('msgr_threads.id'), unique=True)
    umtStatus       = Column(ChoiceType(TYPE_STATUS), default=0)
    last_msg_sent   = Column(DateTime)
    last_visit      = Column(DateTime)
    new_msgs        = Column(Integer)

    def __init__(self, user, msgr_thread, status, last_msg_sent=None,
                 last_visit=None, new_msgs=None):
        self.user_id = user
        self.msgr_threads_id = msgr_thread
        self.last_msg_sent = last_msg_sent
        self.last_visit = last_visit
        self.new_msgs = new_msgs

    def __repr__(self):
        return "<UsersMsgrThreads({} {})>".format(self.user_id, self.msgr_threads_id)
