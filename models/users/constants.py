# coding: utf-8
APP_USERS_GENDER_MAN = u'm'
APP_USERS_GENDER_WOMAN = u'f'
APP_USERS_GENDER_UNDEF = u'n'

APP_USERS_TYPE_GENDER = (
    (APP_USERS_GENDER_MAN, u'Мужской'),
    (APP_USERS_GENDER_WOMAN, u'Женский'),
    (APP_USERS_GENDER_UNDEF, u'Не установлен'),
)


APP_USERSRELS_TYPE_UNDEF = 0
APP_USERSRELS_TYPE_FRIEND = 9
APP_USERSRELS_TYPE_SEND_TO = 1
APP_USERSRELS_TYPE_FROM_USER = 2

APP_USERSRELS_TYPE = (
    (APP_USERSRELS_TYPE_UNDEF, u'Нет'),
    # это когда сам юзер отправил запрос
    (APP_USERSRELS_TYPE_SEND_TO, u'Запрос отправлен'),
    # это когда ему другой юзер отправил
    (APP_USERSRELS_TYPE_FROM_USER, u'Запрос отправлен пользователем'),
    (APP_USERSRELS_TYPE_FRIEND, u'Обоюдная дружба'),
)

