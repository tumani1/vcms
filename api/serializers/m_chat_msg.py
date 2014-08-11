#coding:utf-8
from api.serializers import mUserShort
from models import Users


class mChatMsgSerializer(object):  # TODO: просмотреть как вызываются sql запросы

    def __init__(self, chat_messages, session):
        self.chat_messages = chat_messages
        self.session = session
        self.users = session.query(Users).filter(Users.id.in_((cm.user_id for cm in chat_messages)))

    def get_data(self):
        cms = []
        for cm in self.chat_messages:
            user = self.users.filter(Users.id==cm.user_id).one()
            cms.append({'id': cm.id,
                        'created': cm.created,
                        'text': cm.text,
                        'user': mUserShort(user, session=self.session).data})
        return cms


# def get_data(self):
#         cms = []
#         for cm in self.chat_messages:
#             user = None
#             for u in self.users:
#                 if u.id == cm.user_id:
#                     user = u
#                     break
#             cms.append({'id': cm.id,
#                         'created': cm.created,
#                         'text': cm.text,
#                         'user': mUserShort(user, session=self.session).data})
#         return cms