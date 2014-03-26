# coding: utf-8

from django.contrib import admin

from comments.models import Topics, TopicsExtras, TopicsPersonsExtend


class TopicsAdmin(admin.ModelAdmin):
    search_fields = ('id',)

class TopicsExtrasAdmin(admin.ModelAdmin):
    search_fields = ('id',)

class TopicsPersonsExtendAdmin(admin.ModelAdmin):
    search_fields = ('id',)


admin.site.register(Topics, TopicsAdmin)
admin.site.register(TopicsExtras, TopicsExtrasAdmin)
admin.site.register(TopicsPersonsExtend, TopicsPersonsExtendAdmin)


Topics, TopicsExtras, TopicsPersonsExtend
class CommentsAdmin(admin.ModelAdmin):
    search_fields = ('id',)

# Администрирование таблицы комментариев пользователей
class UsersCommentsAdmin(admin.ModelAdmin):
    search_fields = ('id',)


#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Comments, CommentsAdmin)
admin.site.register(UsersComments, UsersCommentsAdmin)

