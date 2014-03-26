# coding: utf-8

from django.db import models
from ..constants import APP_USER_REQ_TYPE


#############################################################################################################
# Модель Пользовательских запросов
class UsersRequests(models.Model):
    user       = models.ForeignKey('Users', verbose_name=u'Пользователи')
    hash       = models.CharField(max_length=60, verbose_name=u'Запрос')
    created    = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    type       = models.SmallIntegerField(choices=APP_USER_REQ_TYPE, verbose_name=u'Тип запроса')
    value      = models.CharField(max_length=255, verbose_name=u'Значение запроса')
    expiration = models.DateTimeField(verbose_name=u'Время истечения')


    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.user.full_name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_requests'
        app_label = 'users'
        verbose_name = u'Запросы пользователя'
        verbose_name_plural = u'Запросы пользователей'
