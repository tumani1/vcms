# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Контента
class Contents(models.Model):
    title    = models.CharField(max_length=255, verbose_name=u'Название')
    text     = models.TextField(verbose_name=u'Описание')
    obj_id   = models.IntegerField(verbose_name=u'Номер объекта')
    obj_type = models.CharField(max_length=255, verbose_name=u'Тип объекта')
    obj_name = models.CharField(max_length=255, verbose_name=u'Название объекта')
    url      = models.URLField(max_length=255, verbose_name=u'Ссылка')


    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.title)

    class Meta:
        # Имя таблицы в БД
        db_table = 'contents'
        app_label = 'contents'
        verbose_name = u'Контент'
        verbose_name_plural = u'Контент'
