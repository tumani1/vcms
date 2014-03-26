# coding: utf-8

from django.db import models


#############################################################################################################
# Модель пользовательских картинок
class UsersPics(models.Model):
    user = models.ForeignKey('Users', verbose_name=u'Пользователь')
    url  = models.CharField(max_length=255, verbose_name=u'Url')


    def __unicode__(self):
        return u'[{0}] {1} : {2}'.format(self.pk, self.user.full_name, self.url)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_pics'
        app_label = 'users'
        verbose_name = u'Картинки пользователя'
        verbose_name_plural = u'Картинки пользователей'
