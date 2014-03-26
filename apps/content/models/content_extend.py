# coding: utf-8

from django.db import models
from content import Content

#############################################################################################################
# Модель Контента
class ContentExtend(models.Model):

    name    = models.CharField(max_length=255, verbose_name=u'Название', primary_key = True)
    content = models.ForeignKey('Content',verbose_name = 'Контент')
    value = models.CharField(max_length=255, verbose_name=u'Значение')
    value_int   = models.IntegerField(verbose_name = 'Численное значение')
    value_text    = models.TextField(verbose_name = 'Текстовое значение')


    def __unicode__(self):
        return u'[{}] {}'.format(self.pk, self.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'content_extend'
        app_label = 'content'
        verbose_name = u'Контент'
        verbose_name_plural = u'Контент'

