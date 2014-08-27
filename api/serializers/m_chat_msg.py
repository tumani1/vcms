#coding:utf-8
from api.serializers import mUserShort
from models import Users
from utils.common import datetime_to_unixtime


class mChatMsgSerializer(object):

    def __init__(self, chat_messages, session):
        self.chat_messages = chat_messages
        self.session = session
        self.users = session.query(Users).filter(Users.id.in_((cm.user_id for cm in chat_messages)))

    def get_data(self):
        cms = []
        for cm in self.chat_messages:
            user = self.users.filter(Users.id==cm.user_id).one()  # Поломается при рассинхронизации сообщений и владельцев
            cms.append({'id': cm.id,
                        'created': datetime_to_unixtime(cm.created),
                        'text': cm.text,
                        'user': mUserShort(instance=user, session=self.session).data})
        return cms

# этот способ как бы должен слать меньше запросов, но на деле выполняется одинаковое время, что и выше
#     def get_data(self):  # TODO: просмотреть как вызываются sql запросы
#             cms = []
#             for cm in self.chat_messages:
#                 user = None
#                 for u in self.users:
#                     if u.id == cm.user_id:
#                         user = u
#                         break
#                 cms.append({'id': cm.id,
#                             'created': cm.created,
#                             'text': cm.text,
#                             'user': mUserShort(instance=user, session=self.session).data})
#             return cms