# coding: utf-8

from django.contrib import admin

from comments.models import Persons,PersonsTopics,PersonsExtras

# Register your models here.
#############################################################################################################
# Администрирование таблицы персон
class PersonsAdmin(admin.ModelAdmin):
    search_fields = ('id',)

# Администрирование таблицы связей персон и тем
class PersonsTopicsAdmin(admin.ModelAdmin):
    search_fields = ('id',)

# Администрирование таблицы дополнительных материалов персон
class PersonsExtrasAdmin(admin.ModelAdmin):
    search_fields = ('id',)


#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Persons, PersonsAdmin)
admin.site.register(PersonsTopics, PersonsTopicsAdmin)
admin.site.register(PersonsExtras,PersonsExtrasAdmin)

