# coding: utf-8

from django.db import models
from ..constants import APP_USER_LOGS_TYPE


#############################################################################################################
# Модель Пользовательских логов
class UsersLogs(models.Model):
    user    = models.ForeignKey('Users', verbose_name=u'Пользователи')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    type    = models.SmallIntegerField(choices=APP_USER_LOGS_TYPE, verbose_name=u'Тип')
    object  = models.CharField(max_length=255, verbose_name=u'Объект')
    text    = models.CharField(max_length=255, verbose_name=u'Текст')

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.user.full_name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_logs'
        app_label = 'users'
        verbose_name = u'Лог пользователя'
        verbose_name_plural = u'Логи пользователей'
