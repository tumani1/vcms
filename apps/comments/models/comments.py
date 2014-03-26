# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Комментария
class Comments(models.Model):
    user_id     = models.IntegerField(max_length=255, verbose_name=u'Пользователь')
    ctext       = models.TextField(verbose_name=u'Текст комментария')
    created     = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    user_id     = models.IntegerField(max_length=255, verbose_name=u'Родительский комментарий')
    obj_id      = models.IntegerField(verbose_name=u'Номер объекта')
    obj_type    = models.CharField(max_length=255, verbose_name=u'Тип объекта')
    obj_name    = models.CharField(max_length=255, verbose_name=u'Название объекта')


    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.user_id)

    class Meta:
        # Имя таблицы в БД
        db_table = 'comments'
        app_label = 'comments'
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'
