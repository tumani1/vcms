# coding: utf-8

from django.db import models
from apps.users.models import Users

#############################################################################################################
# Модель Комментария Пользователя
class UsersComments(models.Model):
    comment = models.ForeignKey('Users', verbose_name=u'Комментарий')
    user    = models.ForeignKey('Users', verbose_name=u'Пользователь')
    uc_status = models.CharField(max_length=255, verbose_name=u'Статус')
    uc_rating = models.IntegerField(max_length=255, verbose_name=u'Рейтинг')

    def __unicode__(self):
        return u'[{}] {}-{}'.format(self.pk, self.user.id, self.comment.id)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_comments'
        app_label = 'comments'
        verbose_name = u'Комментарий Пользователя'
        verbose_name_plural = u'Комментарии Пользователей'

