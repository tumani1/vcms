# coding: utf-8

from django.contrib import admin

from .models import *


#############################################################################################################
# Администрирование таблицы персон
class PersonsAdmin(admin.ModelAdmin):
    search_fields = ('id',)


#############################################################################################################
# Администрирование таблицы связей персон и тем
class PersonsTopicsAdmin(admin.ModelAdmin):
    search_fields = ('id',)


#############################################################################################################
# Администрирование таблицы дополнительных материалов персон
class PersonsExtrasAdmin(admin.ModelAdmin):
    search_fields = ('id',)


#############################################################################################################
# Администрирование таблицы расширения
class UsersPersonsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'person', 'topic', 'rating', 'status', 'updated',)
    list_filter = ('status', 'updated',)
    search_fields = ('user', )
    raw_id_fields = ('user', 'person', 'topic',)


#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Persons, PersonsAdmin)
admin.site.register(PersonsTopics, PersonsTopicsAdmin)
admin.site.register(PersonsExtras,PersonsExtrasAdmin)
admin.site.register(UsersPersons, UsersPersonsAdmin)
