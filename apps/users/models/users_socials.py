# coding: utf-8

from django.db import models
from ..constants import APP_USER_SOCIAL_PHOTO_DIR, APP_USER_SOC_TYPE

#Todo: Нужно использовать абстрактный класс как videobase для foto
#############################################################################################################
# Модель Пользовательской социальности
class UsersSocials(models.Model):
    @property
    def get_upload_to(self):
        return APP_USER_SOCIAL_PHOTO_DIR

    user    = models.ForeignKey('Users', verbose_name=u'Пользователь')
    type    = models.SmallIntegerField(choices=APP_USER_SOC_TYPE, verbose_name=u'Тип соц. сети')
    token   = models.CharField(max_length=255, verbose_name=u'Токен')
    userid  = models.IntegerField(verbose_name=u'')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    photo   = models.ImageField(upload_to=get_upload_to, verbose_name=u'Фото')


    def __unicode__(self):
        return u'[{0}] {1} - {2}'.format(self.pk, self.user.full_name, self.token)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_socials'
        app_label = 'users'
        verbose_name = u'Социальность пользователя'
        verbose_name_plural = u'Социальность пользователей'
