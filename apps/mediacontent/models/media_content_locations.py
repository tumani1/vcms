# coding: utf-8

from django.db import models
from media_content import MediaContent
from cdn import CDN

#############################################################################################################
# Модель Локации Медиа Контента
class MediaContentLocations(models.Model):

    cdnname        = models.ForeignKey('CDN', verbose_name=u'Используемая CDN')
    media_content  = models.ForeignKey('MediaContent', verbose_name=u'Используемая CDN')
    ltype          = models.IntegerField(verbose_name = 'Количество просмотров')
    allow_mobile   = models.BooleanField(verbose_name = 'Разрешение для мобильных устройств')
    allow_smarttv  = models.BooleanField(verbose_name = 'Разрешение для SmartTV')
    allow_external = models.BooleanField(verbose_name = 'Разрешение для внешних ресурсов')
    allow_external = models.BooleanField(verbose_name = 'Разрешение для незарегистрированных пользователей')
    location        = models.CharField(max_length=255, verbose_name=u'Тип медиа контента')
    created        = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    views_cnt      = models.IntegerField(verbose_name = 'Количество просмотров')


    def __unicode__(self):
        return u'[{}] {}-{}'.format(self.pk, self.cdnname,self.media_content.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'media_content_locations'
        app_label = 'media_content'
        verbose_name = u'Локация Медиа Контента'
        verbose_name_plural = u'Локации Медиа Контента'

