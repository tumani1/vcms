# coding: utf-8

from django.db import models

from ..constants import APP_USER_STATUS, APP_USER_TYPE, APP_USER_USERPIC_TYPE


#############################################################################################################
# Модель Пользователей
class Users(models.Model):
    firstname    = models.CharField(max_length=255, verbose_name=u'Имя')
    lastname     = models.CharField(max_length=255, verbose_name=u'Фамилия')
    email        = models.EmailField(max_length=255, unique=True, verbose_name=u'Email')
    status       = models.PositiveSmallIntegerField(choices=APP_USER_STATUS, verbose_name=u'Статус')
    last_visited = models.DateTimeField(auto_now_add=True, verbose_name=u'Последний визит')
    created      = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    time_zone    = models.CharField(max_length=255, verbose_name=u'Временная зона')
    phone        = models.CharField(max_length=255, verbose_name=u'Телефон')
    country      = models.CharField(max_length=255, verbose_name=u'Страна')
    city         = models.CharField(max_length=255, verbose_name=u'Город')
    address      = models.CharField(max_length=255, verbose_name=u'Адрес')
    birth_date   = models.DateField(verbose_name=u'Дата рождения')
    type         = models.SmallIntegerField(choices=APP_USER_TYPE, verbose_name=u'Тип')
    bio          = models.TextField(verbose_name=u'Биография')
    userpic_type = models.SmallIntegerField(null=True, blank=True, default=None, choices=APP_USER_USERPIC_TYPE, verbose_name=u'Тип картинки')
    userpic_id   = models.ForeignKey('UsersPics', default=None, null=True, blank=True, verbose_name=u'Аватар')


    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.full_name)

    @property
    def full_name(self):
        """
        Get full name through a divider
        """
        full_name = u'{0} {1}'.format(self.firstname, self.lastname)
        return full_name.strip()

    class Meta:
        # Имя таблицы в БД
        db_table = 'users'
        app_label = 'users'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'

