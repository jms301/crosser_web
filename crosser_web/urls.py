from django.conf.urls import patterns, include, url
from crosser_frontend.api import *
from crosser_frontend.backapi import *
from tastypie.api import Api


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(SchemeResource())
v1_api.register(SpeciesResource())
v1_api.register(CrossResource())
v1_api.register(PlantResource())
v1_api.register(LocusResource())
v1_api.register(UserResource())
v1_api.register(OutputResource())
 
back_api = Api(api_name='backend')
back_api.register(BackSchemeResource())
back_api.register(BackCrossResource())
back_api.register(BackPlantResource())
back_api.register(BackLocusResource())
back_api.register(BackOutputResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crosser_web.views.home', name='home'),
    # url(r'^crosser_web/', include('crosser_web.foo.urls')),

    #Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #Uncomment the next line to enable the admin:
    url(r'^su-config/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^api/', include(back_api.urls)),
    #crosser frontend as default
    url(r'^', include('crosser_frontend.urls')),
    url(r'^', include('django.contrib.auth.urls')),
)
