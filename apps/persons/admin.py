# coding: utf-8

from django.contrib import admin

from .models import *


#############################################################################################################
# Администрирование таблицы персон
class PersonsAdmin(admin.ModelAdmin):
    search_fields = ('id',)


#############################################################################################################
# Администрирование таблицы дополнительных материалов персон
class PersonsExtrasAdmin(admin.ModelAdmin):
    search_fields = ('id',)


#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Persons, PersonsAdmin)
admin.site.register(PersonsExtras,PersonsExtrasAdmin)
