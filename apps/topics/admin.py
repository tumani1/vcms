# coding: utf-8

from django.contrib import admin

from .models import *

class TopicsAdmin(admin.ModelAdmin):
    search_fields = ('id',)

class TopicsExtrasAdmin(admin.ModelAdmin):
    search_fields = ('id',)

class TopicsPersonsExtendAdmin(admin.ModelAdmin):
    search_fields = ('id',)


#############################################################################################################
# Администрирование таблицы расширения
class UsersPersonsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'person', 'topic', 'rating', 'status', 'updated',)
    list_filter = ('status', 'updated',)
    search_fields = ('user', )
    raw_id_fields = ('user', 'person', 'topic',)


#############################################################################################################
# Администрирование таблицы связей персон и тем
class PersonsTopicsAdmin(admin.ModelAdmin):
    search_fields = ('id',)


#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Topics, TopicsAdmin)
admin.site.register(TopicsExtras, TopicsExtrasAdmin)
admin.site.register(TopicsPersonsExtend, TopicsPersonsExtendAdmin)
admin.site.register(PersonsTopics, PersonsTopicsAdmin)
admin.site.register(UsersPersons, UsersPersonsAdmin)
