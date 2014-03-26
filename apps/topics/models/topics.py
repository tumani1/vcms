# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Расширения персоны
class Topics(models.Model):
    name           = models.CharField(max_length=255,verbose_name=u'Имя', primary_key = True)
    title          = models.CharField(max_length=255,verbose_name=u'Название' )
    title_orig     = models.CharField(max_length=255,verbose_name=u'Оригинальное название')
    description    = models.TextField(verbose_name=u'Описание')
    release_date   = models.DateField(verbose_name=u'Дата выхода')
    s_status       = models.CharField(max_length=255,verbose_name=u'Статус')
    user_scheme    = models.CharField(max_length=255,verbose_name=u'Схема пользователя')
    person_scheme  = models.CharField(max_length=255,verbose_name=u'Схема персоны')
    content_scheme = models.CharField(max_length=255,verbose_name=u'Схема контента')



    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'topics'
        app_label = 'topics'
        verbose_name = u'Тема'
        verbose_name_plural = u'Темы'

