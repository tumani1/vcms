from api.users.serializer import mUserShort


class mChatMsgSerializer(object):

    def __init__(self, chat_messages, user):
        self.chat_messages = chat_messages
        self.user = user

    def get_data(self):
        cms = []
        for cm in self.chat_messages:
            cms.append({'id': cm.id,
                        'created': cm.created,
                        'text': cm.text,
                        'user': mUserShort(self.user).data})
        return cms