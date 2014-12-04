# coding: utf-8

################################################################################
OBJECT_TYPE_CONTENT = u'c'
OBJECT_TYPE_PERSON = u'p'
OBJECT_TYPE_MEDIA = u'm'
OBJECT_TYPE_MEDIA_UNIT = u'mu'
OBJECT_TYPE_STRIP = u's'
OBJECT_TYPE_TOPIC = u't'

OBJECT_TYPES = (
    (OBJECT_TYPE_CONTENT, u'Контент'),
    (OBJECT_TYPE_PERSON, u'Персона'),
    (OBJECT_TYPE_MEDIA, u'Медиа'),
    (OBJECT_TYPE_MEDIA_UNIT, u'Медиаюнит'),
    (OBJECT_TYPE_STRIP, u'Лента'),
)

CONTENT_OBJECT_TYPES = OBJECT_TYPES + (
    (OBJECT_TYPE_TOPIC, u'Топик'),
)
