# coding: utf-8

from django.db import models
from content import Content

#############################################################################################################
# Модель Контента
class ContentExtend(models.Model):

    name    = models.CharField(max_length=255, verbose_name=u'Название')
    tstatus = models.CharField(max_length=255, verbose_name=u'Статус')

    def __unicode__(self):
        return u'[{}] {}'.format(self.pk, self.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'tags'
        app_label = 'content'
        verbose_name = u'Тэг'
        verbose_name_plural = u'Тэги'
