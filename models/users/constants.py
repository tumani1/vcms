# coding: utf-8

##############################################################
APP_USERS_GENDER_MAN = u'm'
APP_USERS_GENDER_WOMAN = u'f'
APP_USERS_GENDER_UNDEF = u'n'

APP_USERS_TYPE_GENDER = (
    (APP_USERS_GENDER_MAN, u'Мужской'),
    (APP_USERS_GENDER_WOMAN, u'Женский'),
    (APP_USERS_GENDER_UNDEF, u'Не установлен'),
)

APP_USERS_TYPE_BLOCKED = (
    (0, u'нет блокировки'),
    (1, u'блокировка партнёра'),
    (2, u'блокировка от партнёра'),
    (3, u'обоюдная блокировка'),
)

##############################################################
APP_USERSRELS_TYPE_UNDEF = u'u'
APP_USERSRELS_TYPE_FRIEND = u'f'
APP_USERSRELS_TYPE_SEND_TO = u's'
APP_USERSRELS_TYPE_RECIEVE_USER = u'r'

APP_USERSRELS_TYPE = (
    (APP_USERSRELS_TYPE_UNDEF, u'Нет'),
    # это когда сам юзер отправил запрос
    (APP_USERSRELS_TYPE_SEND_TO, u'Запрос отправлен'),
    # это когда ему другой юзер отправил
    (APP_USERSRELS_TYPE_RECIEVE_USER, u'Запрос отправлен пользователем'),
    (APP_USERSRELS_TYPE_FRIEND, u'Обоюдная дружба'),
)


APP_USERSOCIAL_TYPE_VK = u'vk'
APP_USERSOCIAL_TYPE_GOOGLE = u'g+'
APP_USERSOCIAL_TYPE_TWITTER = u'tw'
APP_USERSOCIAL_TYPE_FACEBOOK = u'fb'

APP_USERSOCIAL_TYPE = (
    (APP_USERSOCIAL_TYPE_VK, u'Вконтакте'),
    (APP_USERSOCIAL_TYPE_GOOGLE, u'Google+'),
    (APP_USERSOCIAL_TYPE_FACEBOOK, u'Facebook'),
    (APP_USERSOCIAL_TYPE_TWITTER, u'Twitter'),
)