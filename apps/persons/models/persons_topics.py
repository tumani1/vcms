# coding: utf-8

from django.db import models
from persons import Persons
from apps.topics.models import Topics


#############################################################################################################
# Модель Связь Персоны и Темы
class PersonsTopics(models.Model):
    person      = models.ForeignKey('Persons', max_length=255, verbose_name=u'Персона')
    topic       = models.ForeignKey('Topics', max_length=255, verbose_name=u'Топик')
    t_type      = models.CharField(max_length=255, verbose_name=u'Тип топика')
    t_character = models.CharField(max_length=255, verbose_name=u'Характеристика топика')
    description = models.TextField(verbose_name=u'Описание')


    def __unicode__(self):
        return u'[{}] {}-{}'.format(self.pk, self.person.get_full_name, self.topic.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'persons_topics'
        app_label = 'persons'
        verbose_name = u'Связь персоны и темы'
        verbose_name_plural = u'Связи персон и тем'
        
