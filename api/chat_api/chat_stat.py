from models import Users, SessionToken, Persons


def get_chat_stat(auth_user, session, **kwargs):
    chat = kwargs['chat']

    data = {}
    users = session.query(Users).filter(Users.users_chat==chat)
    on_users = SessionToken.filter_users_is_online(True, users)
    on_users_count = on_users.count()
    persons = session.query(Persons).filter(Persons.user_id.in_([u.id for u in on_users]))

    if auth_user:
        new_msgs_count =
