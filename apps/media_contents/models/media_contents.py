# coding: utf-8

from django.db import models
from apps.contents.models import Tags


#############################################################################################################
# Модель Медиа Контента
class MediaContents(models.Model):
    name           = models.CharField(max_length=255, verbose_name=u'Название')
    name_orig      = models.CharField(max_length=255, verbose_name=u'Оригинальное название')
    allow_mobile   = models.BooleanField(verbose_name=u'Разрешение для мобильных устройств')
    allow_smarttv  = models.BooleanField(verbose_name=u'Разрешение для SmartTV')
    allow_external = models.BooleanField(verbose_name=u'Разрешение для внешних ресурсов')
    allow_external = models.BooleanField(verbose_name=u'Разрешение для незарегистрированных пользователей')
    description    = models.TextField(verbose_name=u'Описание')
    created        = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    views_cnt      = models.IntegerField(verbose_name=u'Количество просмотров')
    mc_type        = models.CharField(max_length=255, verbose_name=u'Тип медиа контента')
    p_status       = models.CharField(max_length=255, verbose_name=u'Статус')
    bio            = models.TextField(verbose_name=u'Биография')
    tags           = models.ManyToManyField(Tags, related_name='contents_tags')


    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'media_contents'
        app_label = 'media_contents'
        verbose_name = u'Медиа Контент'
        verbose_name_plural = u'Медиа Контент'
