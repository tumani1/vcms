# coding: utf-8

APP_STREAM_TYPE_MEDIA_L = u'media-l'
APP_STREAM_TYPE_MUNIT_S = u'munit-s'
APP_STREAM_TYPE_FILM_NW = u'film-nw'
APP_STREAM_TYPE_MEDIA_C = u'media-c'
APP_STREAM_TYPE_PERS_S = u'pers-s'
APP_STREAM_TYPE_PERS_O = u'pers-o'
APP_STREAM_TYPE_USER_A = u'user-a'
APP_STREAM_TYPE_USER_F = u'user-f'
APP_STREAM_TYPE_SYS_A = u'sys-a'

APP_STREAM_TYPE = (
    (APP_STREAM_TYPE_MEDIA_L, u'Поставлен лайк медиа'),
    (APP_STREAM_TYPE_MUNIT_S, u'Подписка на медиа-юнит'),
    (APP_STREAM_TYPE_FILM_NW, u'Установлен признак “не смотреть”'),
    (APP_STREAM_TYPE_MEDIA_C, u'Комментарий к медиа'),
    (APP_STREAM_TYPE_PERS_S, u'Подписка на персону'),
    (APP_STREAM_TYPE_PERS_O, u'Появление медиа-материала с участием персоны'),
    (APP_STREAM_TYPE_USER_A, u'Предложение дружить'),
    (APP_STREAM_TYPE_USER_F, u'Юзеры друзья'),
    (APP_STREAM_TYPE_SYS_A, u'Системное сообщение'),
)

APP_STREAM_TYPE_WITHOUT_USER = (APP_STREAM_TYPE_PERS_O, APP_STREAM_TYPE_SYS_A, )