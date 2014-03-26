# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Контента
class Content(models.Model):

    ctitle   = models.CharField(max_length=255, verbose_name=u'Название')
    ctext    = models.TextField(verbose_name = 'Описание')
    obj_id   = models.IntegerField(verbose_name = 'Номер объекта')
    obj_type = models.CharField(max_length=255, verbose_name=u'Тип объекта')
    obj_name = models.CharField(max_length=255, verbose_name=u'Название объекта')
    url      = models.URLField(max_length=255, verbose_name=u'Ссылка')

    def __unicode__(self):
        return u'[{}] {}'.format(self.pk, self.ctitle)

    class Meta:
        # Имя таблицы в БД
        db_table = 'content'
        app_label = 'content'
        verbose_name = u'Контент'
        verbose_name_plural = u'Контент'

