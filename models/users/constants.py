# coding: utf-8

##############################################################
APP_USERS_GENDER_MAN = u'm'
APP_USERS_GENDER_WOMAN = u'f'
APP_USERS_GENDER_UNDEF = u'n'

APP_USERS_GENDER_DEFAULT = (
    APP_USERS_GENDER_UNDEF, u'Не установлен'
)

APP_USERS_TYPE_GENDER = (
    (APP_USERS_GENDER_MAN, u'Мужской'),
    (APP_USERS_GENDER_WOMAN, u'Женский'),
    (APP_USERS_GENDER_UNDEF, u'Не установлен'),
)
##############################################################
APP_USERSRELS_BLOCK_TYPE_UNDEF = u'0'
APP_USERSRELS_BLOCK_TYPE_SEND = u'1'
APP_USERSRELS_BLOCK_TYPE_RECIEVE = u'2'
APP_USERSRELS_BLOCK_TYPE_MATUALLY = u'3'

APP_USERSRELS_TYPE_BLOCKED = (
    (APP_USERSRELS_BLOCK_TYPE_UNDEF, u'нет блокировки'),
    (APP_USERSRELS_BLOCK_TYPE_SEND, u'блокировка партнёра'),
    (APP_USERSRELS_BLOCK_TYPE_RECIEVE, u'блокировка от партнёра'),
    (APP_USERSRELS_BLOCK_TYPE_MATUALLY, u'обоюдная блокировка'),
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

##############################################################
APP_USER_STATUS_ACTIVE = u'active'
APP_USER_STATUS_BLOCKED = u'blocked'
APP_USER_STATUS_NOT_SUB = u'notsub'

APP_USER_STATUS_TYPE_DEFAULT = (
    APP_USER_STATUS_NOT_SUB, u'Не подтверждён',
)

APP_USER_STATUS_TYPE = (
    (APP_USER_STATUS_ACTIVE, u'Активен'),
    (APP_USER_STATUS_BLOCKED, u'Блокирован'),
    (APP_USER_STATUS_NOT_SUB, u'Не подтверждён'),
)