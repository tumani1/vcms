# coding: utf-8

from django.db import models
from ..constants import APP_USER_REL_STATUS


################################################################################
# Модель Пользовательских отношений
class UsersRels(models.Model):
    user    = models.ForeignKey('Users', verbose_name=u'Пользователь')
    partner = models.ForeignKey('Users', verbose_name=u'Партнер', related_name='partner')
    status  = models.SmallIntegerField(choices=APP_USER_REL_STATUS, verbose_name=u'Тип отношений')
    updated = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания/обновления')


    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.user.full_name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_rels'
        app_label = 'users'
        verbose_name = u'Отношения пользователей'
        verbose_name_plural = u'Отношения пользователей'
