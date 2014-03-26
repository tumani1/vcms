# coding: utf-8

from django.db import models
from apps.persons.models import Persons
from topics import Topics


#############################################################################################################
# Модель Дополнений к связям Персон и Тем
class TopicsPersonsExtend(models.Model):
    name        = models.TextField(verbose_name=u'Имя')
    person      = models.ForeignKey('Persons', max_length=255, verbose_name=u'Персона')
    topic       = models.ForeignKey('Topics', max_length=255, verbose_name=u'Топик')
    value       = models.CharField(max_length=255, verbose_name=u'Строка')
    value_int   = models.IntegerField(max_length=255, verbose_name=u'Число')
    value_text  = models.TextField(verbose_name=u'Текст')


    def __unicode__(self):
        return u'[{}] {}-{}'.format(self.pk, self.person.get_full_name, self.topic.name)


    class Meta:
        # Имя таблицы в БД
        db_table = 'topics_persons_extend'
        app_label = 'topics'
        verbose_name = u'Дополненние к связи персоны и темы'
        verbose_name_plural = u'Дополнения к связям персон и тем'

