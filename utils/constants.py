# coding: utf-8

# STATUS CODE
HTTP_OK = 200

HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_INTERNAL_SERVER_ERROR = 500


#VK SOCIAL AUTH
VK_CLIENT_ID = 4643948
VK_SECRET_KEY = 'qa9kXSjeRTMybQCh6J2I'
VK_REDIRECT_URI = 'http://serialov.tv/login/complete/vk-oauth2'

#OK SOCIAL AUTH
OK_CLIENT_ID = 1111175424
OK_SECRET_KEY = 'F26F415CA79701D85F0F46FC'
OK_PUBLIC_KEY = 'CBACDMDDEBABABABA'
OK_REDIRECT_URI = 'http://serialov.tv/login/complete/ok-oauth2'


################################################################################
OBJECT_TYPE_CONTENT = u'c'
OBJECT_TYPE_PERSON = u'p'
OBJECT_TYPE_MEDIA = u'm'
OBJECT_TYPE_MEDIA_UNIT = u'mu'
OBJECT_TYPE_STRIP = u's'
OBJECT_TYPE_TOPIC = u't'
OBJECT_TYPE_NEWS = u'n'

OBJECT_TYPES = (
    (OBJECT_TYPE_CONTENT, u'Контент'),
    (OBJECT_TYPE_PERSON, u'Персона'),
    (OBJECT_TYPE_MEDIA, u'Медиа'),
    (OBJECT_TYPE_MEDIA_UNIT, u'Медиаюнит'),
    (OBJECT_TYPE_STRIP, u'Лента'),
    (OBJECT_TYPE_NEWS, u'Новости'),
    (OBJECT_TYPE_TOPIC, u'Топик'),
)
