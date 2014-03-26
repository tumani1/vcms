# coding: utf-8

from django.db import models
from apps.media_contents.models import MediaContents


#############################################################################################################
# Модель Персон
class Persons(models.Model):
    firstname     = models.CharField(max_length=255, verbose_name=u'Имя')
    lastname      = models.CharField(max_length=255, verbose_name=u'Фамилия')
    p_status      = models.CharField(max_length=255, verbose_name=u'Статус')
    bio           = models.TextField(verbose_name=u'Биография')
    media_content = models.ManyToManyField(MediaContents, related_name='media_content_persons')


    @property
    def full_name(self):
        full_name = u"{0} ({1})".format(self.firstname, self.lastname)
        return full_name.strip()

    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.full_name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'persons'
        app_label = 'persons'
        verbose_name = u'Персона'
        verbose_name_plural = u'Персоны'
