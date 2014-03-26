# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Контента
class Tags(models.Model):
    name   = models.CharField(max_length=255, verbose_name=u'Название')
    status = models.CharField(max_length=255, verbose_name=u'Статус')


    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'tags'
        app_label = 'contents'
        verbose_name = u'Тэг'
        verbose_name_plural = u'Тэги'
