# coding: utf-8

from django.contrib import admin

from .models import*

# Register your models here.
#############################################################################################################
# Администрирование таблицы комментариев
class CommentsAdmin(admin.ModelAdmin):
    search_fields = ('id',)

# Администрирование таблицы комментариев пользователей
class UsersCommentsAdmin(admin.ModelAdmin):
    search_fields = ('id',)


#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Comments, CommentsAdmin)
admin.site.register(UsersComments, UsersCommentsAdmin)

