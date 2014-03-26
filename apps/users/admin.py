# coding: utf-8

from django.contrib import admin

from .models import *


#############################################################################################################
# Администрирование таблицы пользователей
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'email', 'created', 'type',)
    search_fields = ('id', 'firstname', 'lastname', 'email',)
    list_filter = ('created', 'type', 'userpic_type',)


#############################################################################################################
# Администрирование таблицы соц. регистрации
class UsersSocialsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'created',)
    list_filter = ('type', 'created',)
    search_fields = ('user',)
    raw_id_fields = ('user',)


#############################################################################################################
# Администрирование таблицы логов
class UsersLogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'type', 'created',)
    list_filter = ('type', 'created',)
    search_fields = ('user',)
    raw_id_fields = ('user',)


#############################################################################################################
# Администрирование таблицы расширения
class UsersExtrasAdmin(admin.ModelAdmin):
    list_display = ('id', 'cdn_name', 'location', 'type', 'created',)
    list_filter = ('type', 'created',)
    search_fields = ('user',)
    raw_id_fields = ('user',)


#############################################################################################################
# Администрирование таблицы расширения
class UsersRequestsAdmin(admin.ModelAdmin):
    readonly_fields = UsersRequests._meta.get_all_field_names()
    list_display = ('id', 'type', 'created',)
    list_filter = ('type', 'created',)
    search_fields = ('user',)
    raw_id_fields = ('user',)


#############################################################################################################
# Администрирование таблицы расширения
class UsersRelsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'partner', 'status', 'updated',)
    list_filter = ('status', 'updated',)
    search_fields = ('user',)
    raw_id_fields = ('user', 'partner',)


#############################################################################################################
# Администрирование таблицы расширения
class UsersPicsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'url',)
    search_fields = ('user',)
    raw_id_fields = ('user',)


#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Users, UsersAdmin)
admin.site.register(UsersSocials, UsersSocialsAdmin)
admin.site.register(UsersLogs, UsersLogsAdmin)
admin.site.register(UsersExtras, UsersExtrasAdmin)
admin.site.register(UsersRequests, UsersRequestsAdmin)
admin.site.register(UsersRels, UsersRelsAdmin)
admin.site.register(UsersPics, UsersPicsAdmin)
