from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'agenda.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_URL}),
    url(r'^annotated/css/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_URL}),
    url(r'^agenda$', "cms_users_put.views.all_no"),
    url(r'^annotated$', "cms_users_put.views.all_template"),
    url(r'^agenda/(.*)$', "cms_users_put.views.number_no"),
    url(r'^annotated/(.*)$', "cms_users_put.views.number_template"),
    url(r'^(.*)$', "cms_users_put.views.notfound"),
)
