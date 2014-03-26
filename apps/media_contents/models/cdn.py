# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Локации Медиа Контента
class CDN(models.Model):
    name            = models.CharField(max_length=255, verbose_name=u'Имя', primary_key=True)
    description     = models.CharField(max_length=255, verbose_name=u'Описание')
    has_mobile      = models.BooleanField(verbose_name=u'Имеется ли доступ с мобильных устройств')
    has_auth        = models.BooleanField(verbose_name=u'Имеется ли аутентификация')
    url             = models.URLField(max_length=255, verbose_name=u'Ссылка')
    location_regexp = models.CharField(max_length=255, verbose_name=u'Регулярное выражение')


    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'cdn'
        app_label = 'media_contents'
        verbose_name = u'Медиа Контент'
        verbose_name_plural = u'Медиа Контент'

