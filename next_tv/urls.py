# coding: utf-8
from django.conf.urls import patterns, include, url
from next_tv import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin_tools/', include('admin_tools.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                   )

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}),
    )
