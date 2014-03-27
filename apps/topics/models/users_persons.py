# coding: utf-8

from django.db import models
from apps.users.constants import APP_USER_PER_STATUS

from apps.users.models import Users
from apps.persons.models import Persons


#############################################################################################################
# Модель Пользовательской социальности
class UsersPersons(models.Model):
    user        = models.ForeignKey(Users, verbose_name=u'Пользователь')
    person      = models.ForeignKey(Persons, verbose_name=u'Персона')
    topic       = models.ForeignKey('Topics', verbose_name=u'Топик')
    updated     = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    rating      = models.FloatField(verbose_name=u'Рейтинг')
    status      = models.SmallIntegerField(choices=APP_USER_PER_STATUS, verbose_name=u'Статус')


    def __unicode__(self):
        return u'[{0}] {1}:{2}:{3}'.format(self.pk, self.user.full_name, self.person, self.topic)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_persons'
        app_label = 'topics'
        verbose_name = u' пользователя'
        verbose_name_plural = u' пользователей'
