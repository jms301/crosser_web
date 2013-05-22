from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crosser_web.views.home', name='home'),
    # url(r'^crosser_web/', include('crosser_web.foo.urls')),

    #Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #Uncomment the next line to enable the admin:
    url(r'^su-config/', include(admin.site.urls)),

    #crosser frontend as default
    url(r'^', include('crosser_frontend.urls')),
    url(r'^', include('django.contrib.auth.urls')),
)
