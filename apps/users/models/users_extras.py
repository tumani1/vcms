# coding: utf-8

from django.db import models
from ..constants import APP_USER_EXTRAS_TYPE


#############################################################################################################
# Модель Пользовательских расширений
class UsersExtras(models.Model):
    user        = models.ForeignKey('Users', verbose_name=u'Пользователь')
    type        = models.SmallIntegerField(choices=APP_USER_EXTRAS_TYPE, verbose_name=u'Тип')
    created     = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    cdn_name    = models.CharField(max_length=100, verbose_name=u'CDN')
    location    = models.CharField(max_length=255, verbose_name=u'Месторасположение')
    description = models.TextField(verbose_name=u'Описание')


    def __unicode__(self):
        return u'[%s] %s - %s'.format(self.pk, self.user.full_name, self.type)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_extras'
        app_label = 'users'
        verbose_name = u'Расширение пользователя'
        verbose_name_plural = u'Расширения пользователей'
