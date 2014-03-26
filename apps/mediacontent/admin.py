# coding: utf-8

from django.contrib import admin

from mediacontent.models import MediaContent, MediaContentLocations, CDN

# Register your models here.
#############################################################################################################

# Администрирование таблицы Медиа контента
class MediaContentAdmin(admin.ModelAdmin):
    search_fields = ('id',)


# Администрирование таблицы Локаций для медиа контента 
class MediaContentLocationsAdmin(admin.ModelAdmin):
    search_fields = ('id',)

# Администрирование таблицы CDN
class CDNAdmin(admin.ModelAdmin):
    search_fields = ('id',)



#############################################################################################################
# Регистрация моделей в админке
admin.site.register(MediaContent, MediaContentAdmin)
admin.site.register(MediaContentLocations, MediaContentLocationsAdmin)
admin.site.register(CDN, CDNAdmin)

