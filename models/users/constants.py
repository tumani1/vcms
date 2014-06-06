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

##############################################################
APP_USERSRELS_TYPE_UNDEF = u'0'
APP_USERSRELS_TYPE_FRIEND = u'9'
APP_USERSRELS_TYPE_SEND_TO = u'1'
APP_USERSRELS_TYPE_FROM_USER = u'2'

APP_USERSRELS_TYPE = (
    (APP_USERSRELS_TYPE_UNDEF, u'Нет'),
    # это когда сам юзер отправил запрос
    (APP_USERSRELS_TYPE_SEND_TO, u'Запрос отправлен'),
    # это когда ему другой юзер отправил
    (APP_USERSRELS_TYPE_FROM_USER, u'Запрос отправлен пользователем'),
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


APP_USERSEXTRAS_TYPE = (
    ('1', u'Первый тип'),
    ('2', u'Второй тип'),
)