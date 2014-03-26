# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Расширения персоны
class PersonsExtras(models.Model):
    person      = models.ForeignKey('Persons', max_length=255, verbose_name=u'Персона')
    etype       = models.CharField(max_length=255, verbose_name=u'')
    cdn_name    = models.TextField(verbose_name=u'Имя')
    location    = models.TextField(verbose_name=u'Локация')
    created     = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    description = models.TextField(verbose_name=u'Описание')

    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.person.get_full_name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'persons_extras'
        app_label = 'persons'
        verbose_name = u'Расширения персоны'
        verbose_name_plural = u'Расширения персон'

