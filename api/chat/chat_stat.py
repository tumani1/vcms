# coding=utf-8
from models import Users, SessionToken, Persons, UsersChat
from api.persons.serializer import mPersonSerializer as mP


def get_chat_stat(auth_user, session, **kwargs):
    chat = kwargs['chat']

    users = session.query(Users).join(UsersChat).filter(UsersChat.chat_id==chat)
    on_users = SessionToken.filter_users_is_online(True, users)
    on_users_count = on_users.count()
    persons = session.query(Persons).join(Users).filter(Persons.user_id.in_([u.id for u in on_users.all()])).all()
    mp = mP(instance=persons, user=auth_user, session=session)
    p_data = mp.data
    data = {'user_cnt': on_users_count, 'persons': p_data}
    if auth_user:  # TODO: доделать с монгой
        new_msgs_count = 0
        data.update({'new_msgs': new_msgs_count})

    return data