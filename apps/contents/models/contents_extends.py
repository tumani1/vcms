# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Контента
class ContentsExtends(models.Model):
    name       = models.CharField(max_length=255, verbose_name=u'Название', primary_key=True)
    content    = models.ForeignKey('Contents', verbose_name=u'Контент')
    value      = models.CharField(max_length=255, verbose_name=u'Значение')
    value_int  = models.IntegerField(verbose_name=u'Численное значение')
    value_text = models.TextField(verbose_name=u'Текстовое значение')


    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'contents_extends'
        app_label = 'contents'
        verbose_name = u'Контент'
        verbose_name_plural = u'Контент'
